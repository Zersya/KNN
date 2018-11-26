import csv
import math
from ModelData import ModelData as MD
from operator import attrgetter

MDtrain = []            #data train
MDtest = []             #data test

K = 9                   #atur K nya berapa, saya mendapat 4 karena hasil akurasi lebih maksimal pada saat training dengan train Data

trainLen = 800          #total panjang train data, yang perlu di Indeks
trainRata = 210          #pembagian rata pada setiap kelas Y misal [100, 100, 100, 100] 
                                                                #   0    1    2    3
                        #210 untuk maksimal 800 train, karena tidak semuanya 200 pas

usingTestData = True    # True berarti menggunakan Test data, False berarti menggunakan Training data (di split)

def csv_reader():
    with open('DataTrain_Tugas3_AI.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        hitungRata = [0, 0, 0, 0]
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                #set ModelData dari CSV ke Object ModelData
                Model = MD(int(row[0].replace(" ", "")), float(row[1].replace(" ", "")), float(row[2].replace(" ", "")), float(row[3].replace(" ", "")), float(row[4].replace(" ", "")), float(row[5].replace(" ", "")), int(row[6].replace(" ", "")))

                #region melakukan split sama rata pada setiap data (untuk training)
                if Model.Y == 0 and hitungRata[0] < trainRata: 
                    MDtrain.append(Model)
                    hitungRata[0]+=1
                elif Model.Y == 0 and hitungRata[0] >= trainRata and not usingTestData:
                    MDtest.append(Model)

                elif Model.Y == 1 and hitungRata[1] < trainRata: 
                    MDtrain.append(Model)
                    hitungRata[1]+=1
                elif Model.Y == 1 and hitungRata[1] >= trainRata and not usingTestData:
                    MDtest.append(Model)

                elif Model.Y == 2 and hitungRata[2] < trainRata: 
                    MDtrain.append(Model)
                    hitungRata[2]+=1
                elif Model.Y == 2 and hitungRata[2] >= trainRata and not usingTestData:
                    MDtest.append(Model)

                elif Model.Y == 3 and hitungRata[3] < trainRata: 
                    MDtrain.append(Model)
                    hitungRata[3]+=1
                elif Model.Y == 3 and hitungRata[3] >= trainRata and not usingTestData:
                    MDtest.append(Model)
                #endregion

                
                line_count += 1
            if hitungRata[0] == trainRata and hitungRata[1] == trainRata and hitungRata[2] == trainRata and hitungRata[3] == trainRata and line_count-1 == trainLen:
                break

    if usingTestData:
        with open('DataTest_Tugas3_AI.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    #set ModelData dari CSV ke Object ModelData
                    Model = MD(int(row[0].replace(" ", "")), float(row[1].replace(" ", "")), float(row[2].replace(" ", "")), float(row[3].replace(" ", "")), float(row[4].replace(" ", "")), float(row[5].replace(" ", "")), int(-1))
                    MDtest.append(Model)
                    line_count += 1

    print(f'\t{hitungRata} data pada setiap kelas') #hitungan sama rata
    print(f'\tTrain : {len(MDtrain)}, Test : {len(MDtest)}')

    # for x in range(len(MDtest)):
    #     print(f'{MDtrain[x].Index, MDtrain[x].Y}, {MDtest[x].Index, MDtest[x].Y}')
    
def csv_writer(i):
    with open('TebakanTugas'+str(i)+'.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Index', 'X1', 'X2', 'X3', 'X4', 'X5', 'Y'])
        for test in MDtest:
            writer.writerow([test.Index, test.X1, test.X2, test.X3, test.X4, test.X5, test.Y])
                

def prosesJarak():
    dataBenar = 0       #perhitungan data benar saat training
    
    #region melakukan pencarian jarak terdekat dari sekitar masing" DataTest
    for test in MDtest:
        for train in MDtrain:
            x1 = (train.X1 - test.X1)**2
            x2 = (train.X2 - test.X2)**2
            x3 = (train.X3 - test.X3)**2
            x4 = (train.X4 - test.X4)**2
            x5 = (train.X5 - test.X5)**2
            distance = math.sqrt(((x1) + (x2) + (x3) + (x4) + (x5)))
            train.setDistance(round(distance, 2))
        
        #dilakukan sort Ascending sesuai jarak terdekat 
        MDtrain.sort(key=attrgetter('distance'))
        Ys = []
        for train in MDtrain[:K]:
            Ys.append(train.Y)
            # print(f'{train.distance, train.Index, train.Y}')

        #memilih kelas mana yang paling banyak disekitar, sesuai K
        _Ys = {}
        for y in Ys:
            if y in _Ys:
                _Ys[y] += 1
            else:
                _Ys[y] = 1
        #didapat hasil mana yang paling banyak disekitar
        Y_terdekat = sorted(_Ys, key=_Ys.get, reverse=True)
        # print(f'{_Ys}     {Y_terdekat}') 
        # print(f'{test.Index, test.Y, Y_terdekat[0]}')

        #pengecekan train test, lalu kalkulasi berapa % kebenarannya berdasarkan train
        if usingTestData == False:
            if Y_terdekat[0] == test.Y:
                test.setY(Y_terdekat[0])
                dataBenar+=1
            else:
                test.setY('Beda')
        else:
            test.setY(Y_terdekat[0])
        
    if not usingTestData:
        # print(f'{dataBenar} data sama')
        print(f'{K}, {round((dataBenar*100)/len(MDtest), 1)}% data sama')
    
                    
def main():
    
    csv_reader()
    prosesJarak()
    csv_writer(3)

    # for i in range(1, 100):
    #     global K
    #     K = i
    #     csv_reader()
    #     prosesJarak()
    #     csv_writer(3)
    #     MDtest.clear()
    #     MDtrain.clear()


if __name__ == "__main__":
    main()