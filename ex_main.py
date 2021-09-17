import requests
import json
import pandas
import numpy


def parseTyre(tyre):
    if tyre == 'F': return '0'
    if tyre == 'E': return '1'
    if tyre == 'V': return '2'
    if tyre == 'S': return '3'
    if tyre == 'M': return '4'
    if tyre == 'H': return '5'
    return tyre


def getTrackStatus(status):
    if status == 'Y': return 1
    if status == 'S': return 2
    if status == 'R': return 2
    return 0

col=[
    'idGP',
    'driver',
    'lap',
    'trackStatus',
    'position',
    'targetPosition',
    'grid',
    'out',
    'performance',
    'trackTemp',
    'airTemp',
    'raining',
    'windSpeed',
    'humidity',
    'pressure',
    'windDir',
    'tyre',
    'tyreLap',
    'track',
    'team'
    ]

globalDf = pandas.DataFrame(columns=col)


paths = [
    '2018/2018-03-25_Australian_Grand_Prix/2018-03-25_Race/',
    '2018/2018-04-08_Bahrain_Grand_Prix/2018-04-08_Race/',
    '2018/2018-04-15_Chinese_Grand_Prix/2018-04-15_Race/',
    '2018/2018-04-29_Azerbaijan_Grand_Prix/2018-04-29_Race/',
    '2018/2018-05-13_Spanish_Grand_Prix/2018-05-13_Race/',
    '2018/2018-05-27_Monaco_Grand_Prix/2018-05-27_Race/',
    '2018/2018-06-10_Canadian_Grand_Prix/2018-06-10_Race/',
    '2018/2018-06-24_French_Grand_Prix/2018-06-24_Race/',
    '2018/2018-07-01_Austrian_Grand_Prix/2018-07-01_Race/',
    '2018/2018-07-08_British_Grand_Prix/2018-07-08_Race/',
    '2018/2018-07-22_German_Grand_Prix/2018-07-22_Race/',
    '2018/2018-07-29_Hungarian_Grand_Prix/2018-07-29_Race/',
    '2018/2018-08-26_Belgian_Grand_Prix/2018-08-26_Race/',
    '2018/2018-09-02_Italian_Grand_Prix/2018-09-02_Race/',
    '2018/2018-09-16_Singapore_Grand_Prix/2018-09-16_Race/',
    '2018/2018-09-30_Russian_Grand_Prix/2018-09-30_Race/',
    '2018/2018-10-07_Japanese_Grand_Prix/2018-10-07_Race/',
    '2018/2018-10-21_United_States_Grand_Prix/2018-10-21_Race/',
    '2018/2018-10-28_Mexican_Grand_Prix/2018-10-28_Race/',
    '2018/2018-11-11_Brazilian_Grand_Prix/2018-11-11_Race/',
    '2018/2018-11-25_Abu_Dhabi_Grand_Prix/2018-11-25_Race/',

    '2019/2019-03-17_Australian_Grand_Prix/2019-03-17_Race/',
    '2019/2019-03-31_Bahrain_Grand_Prix/2019-03-31_Race/',
    '2019/2019-04-14_Chinese_Grand_Prix/2019-04-14_Race/',
    '2019/2019-04-28_Azerbaijan_Grand_Prix/2019-04-28_Race/',
    '2019/2019-05-12_Spanish_Grand_Prix/2019-05-12_Race/',
    '2019/2019-05-26_Monaco_Grand_Prix/2019-05-26_Race/',
    '2019/2019-06-09_Canadian_Grand_Prix/2019-06-09_Race/',
    '2019/2019-06-23_French_Grand_Prix/2019-06-23_Race/',
    '2019/2019-06-30_Austrian_Grand_Prix/2019-06-30_Race/',
    '2019/2019-07-14_British_Grand_Prix/2019-07-14_Race/',
    '2019/2019-07-28_German_Grand_Prix/2019-07-28_Race/',
    '2019/2019-08-04_Hungarian_Grand_Prix/2019-08-04_Race/',
    '2019/2019-09-01_Belgian_Grand_Prix/2019-09-01_Race/',
    '2019/2019-09-08_Italian_Grand_Prix/2019-09-08_Race/',
    '2019/2019-09-22_Singapore_Grand_Prix/2019-09-22_Race/',
    '2019/2019-09-29_Russian_Grand_Prix/2019-09-29_Race/',
    '2019/2019-10-13_Japanese_Grand_Prix/2019-10-13_Race/',
    '2019/2019-10-27_Mexican_Grand_Prix/2019-10-27_Race/',
    '2019/2019-11-03_United_States_Grand_Prix/2019-11-03_Race/',
    '2019/2019-11-17_Brazilian_Grand_Prix/2019-11-17_Race/',
    '2019/2019-12-01_Abu_Dhabi_Grand_Prix/2019-12-01_Race/',

    '2020/2020-07-05_Austrian_Grand_Prix/2020-07-05_Race/',
    '2020/2020-07-12_Styrian_Grand_Prix/2020-07-12_Race/',
    '2020/2020-07-19_Hungarian_Grand_Prix/2020-07-19_Race/',
    '2020/2020-08-02_British_Grand_Prix/2020-08-02_Race/',
    '2020/2020-08-09_70th_Anniversary_Grand_Prix/2020-08-09_Race/',
    '2020/2020-08-16_Spanish_Grand_Prix/2020-08-16_Race/',
    '2020/2020-08-30_Belgian_Grand_Prix/2020-08-30_Race/',
    '2020/2020-09-06_Italian_Grand_Prix/2020-09-06_Race/',
    '2020/2020-09-13_Tuscan_Grand_Prix/2020-09-13_Race/',
    '2020/2020-09-27_Russian_Grand_Prix/2020-09-27_Race/',
    '2020/2020-10-11_Eifel_Grand_Prix/2020-10-11_Race/',
    '2020/2020-10-25_Portuguese_Grand_Prix/2020-10-25_Race/',
    '2020/2020-11-01_Emilia_Romagna_Grand_Prix/2020-11-01_Race/',
    '2020/2020-11-15_Turkish_Grand_Prix/2020-11-15_Race/',
    '2020/2020-11-29_Bahrain_Grand_Prix/2020-11-29_Race/',
    '2020/2020-12-06_Sakhir_Grand_Prix/2020-12-06_Race/',
    '2020/2020-12-13_Abu_Dhabi_Grand_Prix/2020-12-13_Race/',

    '2021/2021-03-28_Bahrain_Grand_Prix/2021-03-28_Race/',
    '2021/2021-04-18_Emilia_Romagna_Grand_Prix/2021-04-18_Race/',
    '2021/2021-05-02_Portuguese_Grand_Prix/2021-05-02_Race/',
    '2021/2021-05-09_Spanish_Grand_Prix/2021-05-09_Race/',
    '2021/2021-05-23_Monaco_Grand_Prix/2021-05-23_Race/',
    '2021/2021-06-06_Azerbaijan_Grand_Prix/2021-06-06_Race/',
    '2021/2021-06-20_French_Grand_Prix/2021-06-20_Race/',
    '2021/2021-06-27_Styrian_Grand_Prix/2021-06-27_Race/',
    '2021/2021-07-04_Austrian_Grand_Prix/2021-07-04_Race/',
    '2021/2021-07-18_British_Grand_Prix/2021-07-18_Race/',
    '2021/2021-08-01_Hungarian_Grand_Prix/2021-08-01_Race/',
    '2021/2021-08-29_Belgian_Grand_Prix/2021-08-29_Race/',
    '2021/2021-09-05_Dutch_Grand_Prix/2021-09-05_Race/',
    '2021/2021-09-12_Italian_Grand_Prix/2021-09-12_Race/'
    ]

for pathIdx, path in enumerate(paths):
    print("https://livetiming.formula1.com/static/"+ path +"SPFeed.json")
    response = requests.get("https://livetiming.formula1.com/static/"+ path +"SPFeed.json").content.decode('utf-8-sig')
    data = json.loads(response)
    
    laps = int(data['free']['data']['L'])
    drivers = data['init']['data']['Drivers']

    print(laps)
    print(drivers)

    df = pandas.DataFrame(columns=col)
    
    for idx, driver in enumerate(drivers):
        driverKey = 'p' + driver['Initials']
        laps = data['LapPos']['graph']['data'][driverKey][2:][::2]
        numOfLaps = len(laps)

        if numOfLaps > 0:
            trackStatus = data['LapPos']['graph']['TrackStatus'][2:][1::2]
            positions = data['LapPos']['graph']['data'][driverKey][2:][1::2]
            pTrack = data['Weather']['graph']['data']['pTrack'][1::2]
            pAir = data['Weather']['graph']['data']['pAir'][1::2]
            pRaining = data['Weather']['graph']['data']['pRaining'][1::2]
            pWindSpeed = data['Weather']['graph']['data']['pWind Speed'][1::2]
            pHumidity = data['Weather']['graph']['data']['pHumidity'][1::2]
            pPressure = data['Weather']['graph']['data']['pPressure'][1::2]
            pWindDir = data['Weather']['graph']['data']['pWind Dir'][1::2]
            gridPos = data['LapPos']['graph']['data'][driverKey][1]

            # get performances if exist
            performances = [0]
            if driverKey in data['Scores']['graph']['Performance']:
                performances = data['Scores']['graph']['Performance'][driverKey][1::2]

            # convert to numpy array to allow randomIndices
            pTrack = numpy.array(pTrack)
            pAir = numpy.array(pAir)
            pRaining =  numpy.array(pRaining)
            pWindSpeed = numpy.array(pWindSpeed)
            pHumidity = numpy.array(pHumidity)
            pPressure =  numpy.array(pPressure)
            pWindDir =  numpy.array(pWindDir)

            randomIndices = numpy.sort(numpy.random.choice(len(pTrack), numOfLaps, replace=False))
       
            df2 = pandas.DataFrame(columns=col)
            df2['idGP'] = numpy.full(numOfLaps, pathIdx)
            df2['driver'] = numpy.full(numOfLaps, driver['Initials'])
            df2['team'] = numpy.full(numOfLaps, driver['Team'])
            df2['trackStatus'] = list(map(getTrackStatus, trackStatus))[:numOfLaps]
            df2['lap'] = laps
            df2['targetPosition'] = positions
            df2['grid'] = numpy.full(numOfLaps, gridPos, dtype=int)
            df2['position'] = df2['targetPosition'].shift(1, fill_value=int(gridPos))
            df2['performance'] = numpy.resize(performances, numOfLaps)
            df2['trackTemp'] = pTrack[randomIndices]
            df2['airTemp'] = pAir[randomIndices]
            df2['raining'] = pRaining[randomIndices]
            df2['windSpeed'] = pWindSpeed[randomIndices]
            df2['humidity'] = pHumidity[randomIndices]
            df2['pressure'] = pPressure[randomIndices]
            df2['windDir'] = pWindDir[randomIndices]
            df2['out'] = numpy.append(numpy.zeros(numOfLaps-1, int), int(data['free']['data']['DR'][idx]['F'][5]))
            df2['track'] = numpy.full(numOfLaps, data['free']['data']['CL'])

            tyreHistory = list(list(filter(None, data['xtra']['data']['DR'][idx]['X']))[0])
            tyreHistory.reverse()
            print(tyreHistory)

            tyreStatus = data['xtra']['data']['DR'][idx]['TI']

            a = numpy.empty(0, dtype=int)
            b = []
            for i in range(len(tyreHistory)):
                index = i * 3
                a = numpy.append(a, numpy.arange(tyreStatus[index+2] - tyreStatus[index+1], tyreStatus[index+2], dtype=int))
                b = numpy.append(b, numpy.full(tyreStatus[index+1], tyreHistory[i]))

            #f = [b ** 2 for b in x if b % 2 == 0]

            if(numOfLaps != len(a)):
                a = numpy.resize(a, len(laps))
                b = numpy.resize(b, len(laps))
                print('warning - tyreHistory')

            df2['tyre'] = b
            df2['tyreLap'] = a

            df = df.append(df2)


    if(path.startswith('2018')):
        df['tyre'] = df['tyre'].apply(parseTyre)
        tyreSet = sorted(df['tyre'].unique())
        tyreSet= list(filter(lambda x: x != '', tyreSet))
        print(tyreSet)
        driversDict = {tyreSet[tyreIdx]: tyre for tyreIdx, tyre in enumerate(['S', 'M', 'H'])}
        print(driversDict)
        df['tyre'] = df['tyre'].apply((lambda x: driversDict[x] if (x in driversDict.keys()) else x ))

    globalDf = globalDf.append(df)

print(globalDf.head(40))
globalDf.to_csv('dataset/global_ex.csv')
