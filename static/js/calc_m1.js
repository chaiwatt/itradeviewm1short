    var upColor = '#00da3c';
    var downColor = '#ec0000';

    function createRawData(backtestOhlc){
        var _data = []
        JSON.parse(backtestOhlc).forEach((ohlc,key) => {
            _data.push({
                    time: ohlc.fields.date,
                    open: ohlc.fields.open,
                    close: ohlc.fields.close,
                    low: ohlc.fields.low,
                    high: ohlc.fields.high,
                    tick: ohlc.fields.tick,
                    index: ohlc.pk,
                })
        });
        return _data;
    }

    function convertOhlcTimeframe(ohlctimeframes,_basedate){
        let ohlc_timeframe_m1 = ohlctimeframes.filter(x => x.fields.timeframe == 1)
        let ohlc_timeframe_m5 = ohlctimeframes.filter(x => x.fields.timeframe == 2)
        let ohlc_timeframe_m15 = ohlctimeframes.filter(x => x.fields.timeframe == 3)
        let ohlc_timeframe_m30 = ohlctimeframes.filter(x => x.fields.timeframe == 4)
        let ohlc_timeframe_h1 = ohlctimeframes.filter(x => x.fields.timeframe == 5)
        let ohlc_timeframe_h4 = ohlctimeframes.filter(x => x.fields.timeframe == 6)
        let ohlc_timeframe_d1 = ohlctimeframes.filter(x => x.fields.timeframe == 7)

        var data_ohlc_timeframe_m1 = []
        var data_ohlc_timeframe_m5 = []
        var data_ohlc_timeframe_m15 = []
        var data_ohlc_timeframe_m30 = []
        var data_ohlc_timeframe_h1 = []
        var data_ohlc_timeframe_h4 = []
        var data_ohlc_timeframe_d1 = []

        ohlc_timeframe_m1.forEach((ohlc,key) => {
            data_ohlc_timeframe_m1.push({
                    time: ohlc.fields.date,
                    open: ohlc.fields.open,
                    close: ohlc.fields.close,
                    low: ohlc.fields.low,
                    high: ohlc.fields.high,
                    tick: ohlc.fields.tick,
                    index: ohlc.pk,
                })
        });

        ohlc_timeframe_m5.forEach((ohlc,key) => {
            data_ohlc_timeframe_m5.push({
                    time: ohlc.fields.date,
                    open: ohlc.fields.open,
                    close: ohlc.fields.close,
                    low: ohlc.fields.low,
                    high: ohlc.fields.high,
                    tick: ohlc.fields.tick,
                    index: ohlc.pk,
                })
        });
        ohlc_timeframe_m15.forEach((ohlc,key) => {
            data_ohlc_timeframe_m15.push({
                    time: ohlc.fields.date,
                    open: ohlc.fields.open,
                    close: ohlc.fields.close,
                    low: ohlc.fields.low,
                    high: ohlc.fields.high,
                    tick: ohlc.fields.tick,
                    index: ohlc.pk,
                })
        });
        ohlc_timeframe_m30.forEach((ohlc,key) => {
            data_ohlc_timeframe_m30.push({
                    time: ohlc.fields.date,
                    open: ohlc.fields.open,
                    close: ohlc.fields.close,
                    low: ohlc.fields.low,
                    high: ohlc.fields.high,
                    tick: ohlc.fields.tick,
                    index: ohlc.pk,
                })
        });
        ohlc_timeframe_h1.forEach((ohlc,key) => {
            data_ohlc_timeframe_h1.push({
                    time: ohlc.fields.date,
                    open: ohlc.fields.open,
                    close: ohlc.fields.close,
                    low: ohlc.fields.low,
                    high: ohlc.fields.high,
                    tick: ohlc.fields.tick,
                    index: ohlc.pk,
                })
        });
        ohlc_timeframe_h4.forEach((ohlc,key) => {
            data_ohlc_timeframe_h4.push({
                    time: ohlc.fields.date,
                    open: ohlc.fields.open,
                    close: ohlc.fields.close,
                    low: ohlc.fields.low,
                    high: ohlc.fields.high,
                    tick: ohlc.fields.tick,
                    index: ohlc.pk,
                })
        });
        ohlc_timeframe_d1.forEach((ohlc,key) => {
            data_ohlc_timeframe_d1.push({
                    time: ohlc.fields.date,
                    open: ohlc.fields.open,
                    close: ohlc.fields.close,
                    low: ohlc.fields.low,
                    high: ohlc.fields.high,
                    tick: ohlc.fields.tick,
                    index: ohlc.pk,
                })
        });

        return createOhlcTimeframesData(_basedate,data_ohlc_timeframe_d1,data_ohlc_timeframe_h4,data_ohlc_timeframe_h1,data_ohlc_timeframe_m30,data_ohlc_timeframe_m15,data_ohlc_timeframe_m5,data_ohlc_timeframe_m1)

    }

    function createOhlcTimeframesData(basedate,data_ohlc_timeframe_d1,data_ohlc_timeframe_h4,data_ohlc_timeframe_h1,data_ohlc_timeframe_m30,data_ohlc_timeframe_m15,data_ohlc_timeframe_m5,data_ohlc_timeframe_m1){
        let currentOhlctimeframe = []
        let d1 = null;
        let h4= null;
        let h1= null;
        let m30= null;
        let m15= null;
        let m5= null;
        let m1= null;
        let d = new Date(basedate);
        let newDateStr = `${d.getUTCFullYear()}-${(d.getUTCMonth()+1).toString().padStart(2, '0')}-${d.getUTCDate().toString().padStart(2, '0')}T00:00:00Z`
        newDate = new Date(newDateStr).getTime(),
        result = data_ohlc_timeframe_d1.filter(d => {
            let time = new Date(d.time).getTime();
            return (newDate == time);
        });
        
        d1 =  {d1 : result[0]} 

        let baseYear = d.getUTCFullYear()
        let baseMonth = d.getUTCMonth()+1
        let baseDay = d.getUTCDate()
        let baseHour = d.getUTCHours()
        let baseMinute = d.getUTCMinutes()

        let only_data_ohlc_timeframe_h4 = []
        let basehour_h4 = parseInt(baseHour/4) * 4
        data_ohlc_timeframe_h4.forEach((ohlc,key) => {
            let test_d = new Date(ohlc.time);
            if(parseInt(baseYear) == parseInt(test_d.getUTCFullYear()) && parseInt(baseMonth) == parseInt(test_d.getUTCMonth()+1) && parseInt(baseDay) == parseInt(test_d.getUTCDate()) && parseInt(basehour_h4) == parseInt(test_d.getUTCHours()) 
            ){
                only_data_ohlc_timeframe_h4.push({
                     h4 : ohlc
                })
            }
        });

        h4 = only_data_ohlc_timeframe_h4[only_data_ohlc_timeframe_h4.length-1]

        let only_data_ohlc_timeframe_h1= []
        let basehour_h1 = parseInt(baseHour)
        let h1_key =0
        data_ohlc_timeframe_h1.forEach((ohlc,key) => {
            let test_d = new Date(ohlc.time);
            if(parseInt(baseYear) == parseInt(test_d.getUTCFullYear()) && parseInt(baseMonth) == parseInt(test_d.getUTCMonth()+1) && parseInt(baseDay) == parseInt(test_d.getUTCDate()) && 
            parseInt(basehour_h1) == parseInt(test_d.getUTCHours()) 
            ){
                h1_key = key
                only_data_ohlc_timeframe_h1.push({
                     h1 : ohlc
                })
            }
        });

        let data_ohlc_timeframe_h1_100data = data_ohlc_timeframe_h1.filter((h1,idx) => idx > (h1_key-100) && idx <= (h1_key))
        h1 = only_data_ohlc_timeframe_h1[only_data_ohlc_timeframe_h1.length-1]
        // ////console.log(h1)

        let only_data_ohlc_timeframe_m30= []
        let baseminute_m30 = parseInt(baseMinute/30) * 30
        let m30_key = 0
        data_ohlc_timeframe_m30.forEach((ohlc,key) => {
            let test_d = new Date(ohlc.time);
            if(parseInt(baseYear) == parseInt(test_d.getUTCFullYear()) 
            && parseInt(baseMonth) == parseInt(test_d.getUTCMonth()+1) 
            && parseInt(baseDay) == parseInt(test_d.getUTCDate())
            && parseInt(baseHour) == parseInt(test_d.getUTCHours())
            && parseInt(baseminute_m30) == parseInt(test_d.getUTCMinutes())
            
            )
            {
                // //console.log(key)
                m30_key = key
                only_data_ohlc_timeframe_m30.push({
                     m30 : ohlc
                })
            }
        });

        // //console.log('This is M30 data')
        // //console.log(data_ohlc_timeframe_m30)
        // //console.log(only_data_ohlc_timeframe_m30)

        let data_ohlc_timeframe_m30_100data = data_ohlc_timeframe_m30.filter((m30,idx) => idx > (m30_key-100) && idx <= (m30_key))
        // //console.log(data_ohlc_timeframe_m30_100data)
        m30 = only_data_ohlc_timeframe_m30[only_data_ohlc_timeframe_m30.length-1]

        ////

        let only_data_ohlc_timeframe_m15= []
        let baseminute_m15 = parseInt(baseMinute/15) * 15
        let m15_key =0
        data_ohlc_timeframe_m15.forEach((ohlc,key) => {
            let test_d = new Date(ohlc.time);
            if(parseInt(baseYear) == parseInt(test_d.getUTCFullYear()) 
            && parseInt(baseMonth) == parseInt(test_d.getUTCMonth()+1) 
            && parseInt(baseDay) == parseInt(test_d.getUTCDate())
            && parseInt(baseHour) == parseInt(test_d.getUTCHours())
            && parseInt(baseminute_m15) == parseInt(test_d.getUTCMinutes())
            ){
                // //console.log(key)
                m15_key =key
                only_data_ohlc_timeframe_m15.push({
                     m15 : ohlc
                })
            }
        });

        // //console.log('This is M15 data')
        // //console.log(data_ohlc_timeframe_m15)
        // //console.log(only_data_ohlc_timeframe_m15)
        let data_ohlc_timeframe_m15_100data = data_ohlc_timeframe_m15.filter((m15,idx) => idx > (m15_key-100) && idx <= (m15_key))
        // //console.log(data_ohlc_timeframe_m15_100data)
        m15 = only_data_ohlc_timeframe_m15[only_data_ohlc_timeframe_m15.length-1]

        let only_data_ohlc_timeframe_m5= []
        let baseminute_m5 = parseInt(baseMinute/5) * 5
        let m5_key =0
        data_ohlc_timeframe_m5.forEach((ohlc,key) => {
            let test_d = new Date(ohlc.time);

            if(parseInt(baseYear) == parseInt(test_d.getUTCFullYear()) 
            && parseInt(baseMonth) == parseInt(test_d.getUTCMonth()+1) 
            && parseInt(baseDay) == parseInt(test_d.getUTCDate())
            && parseInt(baseHour) == parseInt(test_d.getUTCHours())
            && parseInt(baseminute_m5) == parseInt(test_d.getUTCMinutes())
            ){
                // //console.log(key)
                m5_key = key
                only_data_ohlc_timeframe_m5.push({
                     m5 : ohlc
                })
            }
        });

        // //console.log('This is M5 data')
        // //console.log(data_ohlc_timeframe_m5)
        // //console.log(only_data_ohlc_timeframe_m5)

        let data_ohlc_timeframe_m5_100data = data_ohlc_timeframe_m5.filter((m5,idx) => idx > (m5_key-100) && idx <= (m5_key))
        // //console.log(data_ohlc_timeframe_m5_100data)

        m5 = only_data_ohlc_timeframe_m5[only_data_ohlc_timeframe_m5.length-1]


        let only_data_ohlc_timeframe_m1= []
        let baseminute_m1 = parseInt(baseMinute/1) * 1
        let m1_key = 0
        data_ohlc_timeframe_m1.forEach((ohlc,key) => {
            let test_d = new Date(ohlc.time);

            if(parseInt(baseYear) == parseInt(test_d.getUTCFullYear()) 
            && parseInt(baseMonth) == parseInt(test_d.getUTCMonth()+1) 
            && parseInt(baseDay) == parseInt(test_d.getUTCDate())
            && parseInt(baseHour) == parseInt(test_d.getUTCHours())
            && parseInt(baseminute_m1) == parseInt(test_d.getUTCMinutes())
            ){
                m1_key =key
                only_data_ohlc_timeframe_m1.push({
                     m1 : ohlc
                })
            }
        });

        // //console.log('This is M1 data')
        // //console.log(data_ohlc_timeframe_m1)
        // //console.log(only_data_ohlc_timeframe_m1)

        let data_ohlc_timeframe_m1_100data = data_ohlc_timeframe_m1.filter((m1,idx) => idx > (m1_key-100) && idx <= (m1_key))
        // //console.log(data_ohlc_timeframe_m1_100data)
      
        m1 = only_data_ohlc_timeframe_m1[only_data_ohlc_timeframe_m1.length-1]

        let start = parseInt(m1.m1.index) - 1
        numNeed = 5
        let m5from_m1 = data_ohlc_timeframe_m1.filter(x => (x.index >= (start - numNeed +1) && x.index <= start))

        let max_high_m5from_m1 = Math.max.apply(null, m5from_m1.map(item => item.high));
        let min_low_m5from_m1 = Math.min.apply(null, m5from_m1.map(item => item.low));
        let m5from_m1_open = m5from_m1[0].open
        let m5from_m1_close = m5from_m1[m5from_m1.length-1].close

        let m5from_m1_data = {
            open: m5from_m1_open,
            close: m5from_m1_close,
            low: min_low_m5from_m1,
            high: max_high_m5from_m1,
        }

        // //console.log(m5from_m1)
        // //console.log(m5from_m1_data)

        numNeed = 15
        let m15from_m1 = data_ohlc_timeframe_m1.filter(x => (x.index >= (start - numNeed +1) && x.index <= start))
        let max_high_m15from_m1 = Math.max.apply(null, m15from_m1.map(item => item.high));
        let min_low_m15from_m1 = Math.min.apply(null, m15from_m1.map(item => item.low));
        let m15from_m1_open = m15from_m1[0].open
        let m15from_m1_close = m15from_m1[m15from_m1.length-1].close

        let m15from_m1_data = {
            open: m15from_m1_open,
            close: m15from_m1_close,
            low: min_low_m15from_m1,
            high: max_high_m15from_m1,
        }

        // //console.log(m15from_m1)
        // //console.log(m15from_m1_data)

        numNeed = 30
        let m30from_m1 = data_ohlc_timeframe_m1.filter(x => (x.index >= (start - numNeed +1) && x.index <= start))
        let max_high_m30from_m1 = Math.max.apply(null, m30from_m1.map(item => item.high));
        let min_low_m30from_m1 = Math.min.apply(null, m30from_m1.map(item => item.low));
        let m30from_m1_open = m30from_m1[0].open
        let m30from_m1_close = m30from_m1[m30from_m1.length-1].close
 


        let m30from_m1_data = {
            open: m30from_m1_open,
            close: m30from_m1_close,
            low: min_low_m30from_m1,
            high: max_high_m30from_m1,
        }

        ////console.log(m30from_m1_data)

        // //console.log(m30from_m1_data)
        // //console.log(m30from_m1)

        numNeed = 60
        let h1from_m1 = data_ohlc_timeframe_m1.filter(x => (x.index >= (start - numNeed +1) && x.index <= start))
        let max_high_h1from_m1 = Math.max.apply(null, h1from_m1.map(item => item.high));
        let min_low_h1from_m1 = Math.min.apply(null, h1from_m1.map(item => item.low));
        let h1from_m1_open = h1from_m1[0].open
        let h1from_m1_close = h1from_m1[h1from_m1.length-1].close

        // //console.log(h1from_m1)

        let h1from_m1_data = {
            open: h1from_m1_open,
            close: h1from_m1_close,
            low: min_low_h1from_m1,
            high: max_high_h1from_m1,
        }

        // //console.log(h1from_m1)
        // //console.log(h1from_m1_data)

        let m1from_m1 = data_ohlc_timeframe_m1.filter(x => (x.index >= (start - 1 +1) && x.index <= start))[0]

        let m1from_m1_data = {
            open: m1from_m1.open,
            close: m1from_m1.close,
            low: m1from_m1.low,
            high: m1from_m1.high,
        }

        let data_ohlc_timeframe_100data =[]
        data_ohlc_timeframe_100data.push(data_ohlc_timeframe_h1_100data,data_ohlc_timeframe_m30_100data,data_ohlc_timeframe_m15_100data,data_ohlc_timeframe_m5_100data,data_ohlc_timeframe_m1_100data)

        let currentOhlctimeframe_from_m1 =[]
        currentOhlctimeframe_from_m1.push(h1from_m1_data,m30from_m1_data,m15from_m1_data,m5from_m1_data,m1from_m1_data)

        currentOhlctimeframe.push(d1,h4,h1,m30,m15,m5,m1)

        return [currentOhlctimeframe,currentOhlctimeframe_from_m1,data_ohlc_timeframe_100data]
    }

    function getOhlcTimeframesDataFromM1(data){ 
        let _m5from_m1 = data.slice(-5)
        let m5from_m1 = []
        _m5from_m1.forEach((item,key) => {
            m5from_m1.push({
                open: item[0],
                close: item[1],
                low: item[2],
                high: item[3],
            })
        });

        // //console.log(_m5from_m1)

        let max_high_m5from_m1 = Math.max.apply(null, m5from_m1.map(item => item.high));
        let min_low_m5from_m1 = Math.min.apply(null, m5from_m1.map(item => item.low));
        let  m5from_m1_open = m5from_m1[0].open
        let  m5from_m1_close = m5from_m1[m5from_m1.length-1].close

        let m5from_m1_data = {
            open: m5from_m1_open,
            close: m5from_m1_close,
            low: min_low_m5from_m1,
            high: max_high_m5from_m1,
        }


        let _m15from_m1 = data.slice(-15)
        let m15from_m1 = []
        _m15from_m1.forEach((item,key) => {
            m15from_m1.push({
                open: item[0],
                close: item[1],
                low: item[2],
                high: item[3],
            })
        });
        
        let max_high_m15from_m1 = Math.max.apply(null, m15from_m1.map(item => item.high));
        let min_low_m15from_m1 = Math.min.apply(null, m15from_m1.map(item => item.low));
        let  m15from_m1_open = m15from_m1[0].open
        let   m15from_m1_close= m15from_m1[m15from_m1.length-1].close

        let m15from_m1_data = {
            open: m15from_m1_open,
            close: m15from_m1_close,
            low: min_low_m15from_m1,
            high: max_high_m15from_m1,
        }

        // //console.log(m15from_m1)
        // //console.log(m15from_m1_data)

        //=======

        let _m30from_m1 = data.slice(-30)
        let m30from_m1 = []
        _m30from_m1.forEach((item,key) => {
            m30from_m1.push({
                open: item[0],
                close: item[1],
                low: item[2],
                high: item[3],
            })
        });
        
        let max_high_m30from_m1 = Math.max.apply(null, m30from_m1.map(item => item.high));
        let min_low_m30from_m1 = Math.min.apply(null, m30from_m1.map(item => item.low));
        let  m30from_m1_open= m30from_m1[0].open
        let  m30from_m1_close = m30from_m1[m30from_m1.length-1].close

        let m30from_m1_data = {
            open: m30from_m1_open,
            close: m30from_m1_close,
            low: min_low_m30from_m1,
            high: max_high_m30from_m1,
        }

        // //console.log(m30from_m1)
        // //console.log(m30from_m1_data)

        
        //=======

        let _h1from_m1 = data.slice(-60)
        let h1from_m1 = []
        _h1from_m1.forEach((item,key) => {
            h1from_m1.push({
                open: item[0],
                close: item[1],
                low: item[2],
                high: item[3],
            })
        });
        
        let max_high_h1from_m1 = Math.max.apply(null, h1from_m1.map(item => item.high));
        let min_low_h1from_m1 = Math.min.apply(null, h1from_m1.map(item => item.low));
        let  h1from_m1_open= h1from_m1[0].open
        let  h1from_m1_close = h1from_m1[h1from_m1.length-1].close

        let h1from_m1_data = {
            open: h1from_m1_open,
            close: h1from_m1_close,
            low: min_low_h1from_m1,
            high: max_high_h1from_m1,
        }

        // //console.log(h1from_m1)
        // //console.log(h1from_m1_data)


        let m1from_m1_data = {
            open: data[data.length-1][0],
            close: data[data.length-1][1],
            low: data[data.length-1][2],
            high: data[data.length-1][3],
        }

        let currentOhlctimeframe_from_m1 = []

        currentOhlctimeframe_from_m1.push(h1from_m1_data,m30from_m1_data,m15from_m1_data,m5from_m1_data,m1from_m1_data)
        return (currentOhlctimeframe_from_m1)

    }
    
    function getData(_arr) {
        var _data = []
        _arr.forEach((item,key) => {
            let _index = item.index;
            if(typeof _index === "undefined"){
                _index = item.id;
            }
            _data.push(Object.seal([
                item.open,
                item.close,
                item.low,
                item.high,
                _index,
                item.time,
                item.tick,
            ]))
        });
        return _data;
    }

    function createTfData(_arr){
        return [[
            [_arr[6].m1.open,_arr[6].m1.close,_arr[6].m1.low,_arr[6].m1.high,_arr[6].m1.index],
            [_arr[5].m5.open,_arr[5].m5.close,_arr[5].m5.low,_arr[5].m5.high,_arr[5].m5.index],
            [_arr[4].m15.open,_arr[4].m15.close,_arr[4].m15.low,_arr[4].m15.high,_arr[4].m15.index],
            [_arr[3].m30.open,_arr[3].m30.close,_arr[3].m30.low,_arr[3].m30.high,_arr[3].m30.index],
            // [_arr[2].h1.open,_arr[2].h1.close,_arr[2].h1.low,_arr[2].h1.high,_arr[2].h1.index],
            // [_arr[1].h4.open,_arr[1].h4.close,_arr[1].h4.low,_arr[1].h4.high,_arr[1].h4.index],
        ], [_arr[6].m1.time,_arr[5].m5.time,_arr[4].m15.time,_arr[3].m30.time]] 
        //     [_arr[0].d1.open,_arr[0].d1.close,_arr[0].d1.low,_arr[0].d1.high,_arr[0].d1.index],
        // ], [_arr[6].m1.time,_arr[5].m5.time,_arr[4].m15.time,_arr[3].m30.time,_arr[2].h1.time,_arr[1].h4.time,_arr[0].d1.time]] 
    }

    function createTfDataSearch(_arr){
        return [[
            [_arr[4].m1.open,_arr[4].m1.close,_arr[4].m1.low,_arr[4].m1.high],
            [_arr[3].m5.open,_arr[3].m5.close,_arr[3].m5.low,_arr[3].m5.high],
            [_arr[2].m15.open,_arr[2].m15.close,_arr[2].m15.low,_arr[2].m15.high],
            [_arr[1].m30.open,_arr[1].m30.close,_arr[1].m30.low,_arr[1].m30.high],
            // [_arr[0].h1.open,_arr[0].h1.close,_arr[0].h1.low,_arr[0].h1.high],
            // [_arr[0].h4.open,_arr[0].h4.close,_arr[0].h4.low,_arr[0].h4.high],
        ], [_arr[4].m1.time,_arr[3].m5.time,_arr[2].m15.time,_arr[1].m30.time]] 
        //     [_arr[0].d1.open,_arr[0].d1.close,_arr[0].d1.low,_arr[0].d1.high],
        // ], [_arr[6].m1.time,_arr[5].m5.time,_arr[4].m15.time,_arr[3].m30.time,_arr[2].h1.time,_arr[1].h4.time,_arr[0].d1.time]] 
    }

    function createTfDataSearchFromM1(_arr){
        return [[
            [_arr[4].open,_arr[4].close,_arr[4].low,_arr[4].high],
            [_arr[3].open,_arr[3].close,_arr[3].low,_arr[3].high],
            [_arr[2].open,_arr[2].close,_arr[2].low,_arr[2].high],
            [_arr[1].open,_arr[1].close,_arr[1].low,_arr[1].high],
            // [_arr[0].open,_arr[0].close,_arr[0].low,_arr[0].high],
        ], [_arr[4].time,_arr[3].time,_arr[2].time,_arr[1].time]] 
    }

    function createTfFromM15Data(_arr){
        return [
   
            [_arr[4].open,_arr[4].close,_arr[4].low,_arr[4].high],
            [_arr[3].open,_arr[3].close,_arr[3].low,_arr[3].high],
            [_arr[2].open,_arr[2].close,_arr[2].low,_arr[2].high],
            [_arr[1].open,_arr[1].close,_arr[1].low,_arr[1].high],
            // [_arr[0].open,_arr[0].close,_arr[0].low,_arr[0].high],
        ]
    }

    function createTfFromM1Data(_arr){
        return [
            [_arr[6].open,_arr[6].close,_arr[6].low,_arr[6].high],
            [_arr[5].open,_arr[5].close,_arr[5].low,_arr[5].high],
            [_arr[4].open,_arr[4].close,_arr[4].low,_arr[4].high],
            [_arr[3].open,_arr[3].close,_arr[3].low,_arr[3].high],
            [_arr[2].open,_arr[2].close,_arr[2].low,_arr[2].high],
            [_arr[1].open,_arr[1].close,_arr[1].low,_arr[1].high],
        ]
    }


    function getSampleData(_arr) {
        var _data = []
        _arr.forEach((item,key) => {
            _data.push(Object.seal([item.open,item.close,item.low,item.high,key]))
        });
        return _data;
    }

    function getClosedPrice(_arr) {
        var _closedprice = []
        _arr.forEach((item) => {
            _closedprice.push(item.close)
        });
        return _closedprice;
    }

    function getLowPrice(_arr) {
        var _lowprice = []
        _arr.forEach((item) => {
            _lowprice.push(item.low)
        });
        return _lowprice;
    }

    function getHighPrice(_arr) {
        var _highprice = []
        _arr.forEach((item) => {
            _highprice.push(item.high)
        });
        return _highprice;
    }

    function getDateLabel(_arr) {
        var _dateLabel = []
        _arr.forEach((item) => {
            _dateLabel.push(item.time)
        });
        return _dateLabel;
    }

    function getAvgClosedPrice(mArray,mRange){
        return mArray.slice(0, mRange).reduce((a,c) => a + c, 0) / mRange;
    }

    function EMACalc(mArray,mRange) {
        var k = 2/(mRange + 1);
        var avgClosed = getAvgClosedPrice(mArray,mRange)
        emaArray = [avgClosed];
        
        var _emaArray = [];
        for (var i = mRange; i < mArray.length+1; i++) {
            emaArray.push(mArray[i] * k + emaArray[i -mRange] * (1 - k));
            _emaArray.push(emaArray[i-mRange]);
        }
        return _emaArray;
    }

    function SSMA_BARESMOTH(arrSSMA,mRange) {
        _ssmaSmoth = [];
        for (var i = 0; i < arrSSMA.length-mRange+1; i++) {
            var ssmaSmoth = arrSSMA.slice(i, mRange+i).reduce((a,c) => a + c, 0) / mRange;
            _ssmaSmoth.push(ssmaSmoth);
        }
        return _ssmaSmoth;
    }

    function calculateMA(dayCount, data) {
        var result = [];
        for (var i = 0, len = data.length; i < len; i++) {
            if (i < dayCount) {
                result.push('-');
                continue;
            }
            var sum = 0;
            for (var j = 0; j < dayCount; j++) {
                sum += data[i - j][1];
            }
            result.push((sum / dayCount));
        }
        return result;
    }

    function EMACalc(mArray,mRange) {
        var k = 2/(mRange + 1);
        var avgClosed = getAvgClosedPrice(mArray,mRange)
        emaArray = [avgClosed];
        
        var _emaArray = [];
        for (var i = mRange; i < mArray.length+1; i++) {
            emaArray.push(mArray[i] * k + emaArray[i -mRange] * (1 - k));
            _emaArray.push(emaArray[i-mRange]);
        }
        return _emaArray;
    }

    function MACDCalc(mArray1,mArray2,mRange1,mRange2) {
        var diffRange = mRange1 - mRange2;
        var _macdArray = [];
        for (var i = 0; i < mArray1.length; i++) {
            var _macd  = mArray2[i+diffRange] - mArray1[i];
            _macdArray.push(_macd);
        }
        return _macdArray;
    }

    function HistogramCalc(mArray1,mArray2,mRange) {
        var diffRange = mRange - 1;
        var _histogramArray = [];
        for (var i = 0; i < mArray1.length; i++) {
            var _histogram = mArray2[i+diffRange] - mArray1[i];
            _histogramArray.push(_histogram);
        }
        return _histogramArray;
    }

    function SSMA_Calc(arr,n){
        var ssma = [];
        ssma.push(avarageSum(arr,n));

        for (var i = 1 ; i < arr.length ; i++){
            ssma.push((ssma[i-1]*(n-1) + arr[i])/n);
        }
        return ssma;

        function avarageSum(arr,n){
            var temp = arr.slice(0, n);
            return temp.reduce(function(a,b){return a+b;})/temp.length;
        }
    }

    function TenkanSen(highArr,lowArr,n){
        let maxhigharr = []
        let minlowarr = []
        let tenkansenarr = []
        for (let i = 0 ; i < highArr.length-8 ; i++){
            let _highArr = highArr.slice(i, n+i);
            maxhigharr.push(Math.max(..._highArr));
        }

        for (let i = 0 ; i < lowArr.length-8 ; i++){
            let _lowArr = lowArr.slice(i, n+i);
            minlowarr.push(Math.min(..._lowArr));
        }

        for (let i = 0 ; i < maxhigharr.length ; i++){
            tenkansenarr.push((maxhigharr[i] + minlowarr[i])/2)
        }

        // console.log(tenkansenarr)
        return tenkansenarr
    }

    function KijunSen(highArr,lowArr,n){
        let maxhigharr = []
        let minlowarr = []
        let kijunsen = []
        for (let i = 0 ; i < highArr.length-25 ; i++){
            let _highArr = highArr.slice(i, n+i);
            maxhigharr.push(Math.max(..._highArr));
        }

        for (let i = 0 ; i < lowArr.length-25 ; i++){
            let _lowArr = lowArr.slice(i, n+i);
            minlowarr.push(Math.min(..._lowArr));
        }

        for (let i = 0 ; i < maxhigharr.length ; i++){
            kijunsen.push((maxhigharr[i] + minlowarr[i])/2)
        }

        // console.log(kijunsen)
        return kijunsen
    }

    function SenkouSpanA(tenkanSenArr,kijunSenArr){
        let senkouspana = []
        for (let i = 0 ; i < kijunSenArr.length ; i++){
            senkouspana.push((tenkanSenArr[i+17]+kijunSenArr[i])/2)
        }
        return senkouspana
    }

    function SenkouSpanB(highArr,lowArr,n){
        let maxhigharr = []
        let minlowarr = []
        let senkouspanb = []
        for (let i = 0 ; i < highArr.length-26 ; i++){
            let _highArr = highArr.slice(i, n+i);
            maxhigharr.push(Math.max(..._highArr));
        }

        for (let i = 0 ; i < lowArr.length-26 ; i++){
            let _lowArr = lowArr.slice(i, n+i);
            minlowarr.push(Math.min(..._lowArr));
        }

        for (let i = 0 ; i < maxhigharr.length-25 ; i++){
            senkouspanb.push((maxhigharr[i]+minlowarr[i])/2);
        }

        // console.log(senkouspanb)
        return senkouspanb
    }

    function ChikouSpan(closepriceArr){
        let chikouSpan = closepriceArr.slice(25, closepriceArr.length);
        return chikouSpan
    }
    

    function MaxHigh(arr,n){
        let maxarr = []
        for (var i = 0 ; i < arr.length-8 ; i++){
            var temp = arr.slice(i, n+i);
            maxarr.push(Math.max(...temp));
        }
        return maxarr
    }

    function IchimokuCheckUptrend(data,tenkan,kijun,chisou,spanA,spanB){
        let datalow = data[data.length-1][2]
        if(datalow > spanA[spanA.length-26] 
                && datalow > spanB[spanB.length-26] 
                && tenkan[tenkan.length-26] > spanA[spanA.length-26] 
                && tenkan[tenkan.length-26] > spanB[spanB.length-26] 
                && kijun[kijun.length-26] > spanA[spanA.length-26] 
                && kijun[kijun.length-26] > spanB[spanB.length-26] 

            ){
            return true
        }else{
            return false
        }
    }

    function IchimokuCheckDowntrend(data,tenkan,kijun,chisou,spanA,spanB){
        let datahigh = data[data.length-1][3]
        if(datahigh < spanA[spanA.length-26] 
                && datahigh < spanB[spanB.length-26] 
                && tenkan[tenkan.length-26] < spanA[spanA.length-26] 
                && tenkan[tenkan.length-26] < spanB[spanB.length-26] 
                && kijun[kijun.length-26] < spanA[spanA.length-26] 
                && kijun[kijun.length-26] < spanB[spanB.length-26] 

            ){
            return true
        }else{
            return false
        }
    }

    function GetBodySize(arr){
        var bodyArr = [];
        for (var i = 0 ; i < arr.length ; i++){
            if(arr[i][0] == arr[i][1]){
                bodyArr.push(arr[i][0]);
            }else{
                if(arr[i][1] > arr[i][0]){
                    bodyArr.push((arr[i][1]-arr[i][0])/2 + arr[i][0]);
                }else{
                    bodyArr.push((arr[i][0]-arr[i][1])/2 + arr[i][1]);
                }
                
            }
            
        }
        return bodyArr
    }

    function getSignChange(arr,macdarr){
        let positive = arr[0] >= 0; 
        return arr.map((item, index) => {
            if ((positive && item < 0 || !positive && item >= 0)) {
                positive = arr[index] >= 0
                if(arr[index-1]!==null && item !== null){
                    var isUpTrendUpperMacd = '';
                    var macdatpoint = macdarr[index];
                    if(item > 0){
                        if(macdatpoint < 0){
                            isUpTrendUpperMacd = 'under';
                        }else{
                            isUpTrendUpperMacd = 'above';
                        }
                    }
                    return [index-1, arr[index-1], item,isUpTrendUpperMacd]
                }
            }
        }).filter(x => x != null);
    }

    function getMacdCross(macd,signal){
        let isUp = true;
        let crossAbove = true;  
        let crossIndex = 0; 
        if(macd[macd.length-1] > signal[signal.length-1]){ 
            for(var i = macd.length-1 ; i > 0 ; i--){
                if(macd[i] < signal[i]){
                    if(macd[i] < 0){       
                        crossAbove = false
                    }
                    crossIndex = i;
                    break;
                }
            }
        }else{
            isUp = false
            for(var i = macd.length-1 ; i > 0 ; i--){
                if(macd[i] > signal[i]){
                    if(macd[i] < 0){
                        crossAbove = false
                    }
                    crossIndex = i;
                    break;
                }
            }
        }
        return [isUp,crossAbove,crossIndex+1,macd[macd.length-1]]
    }


    function getAllTimeframeTrend(arr,linelenght){
        var slopes = [];
        for (let i = 0; i <= 3; i++) {
            let closedPrice = getClosedPrice(arr[i]);
            let SSMA20Arr = SSMA_Calc(closedPrice,20);
            let regressiveEq = genRegressionLine(SSMA20Arr,linelenght)
            slopes.push(regressiveEq[0]);
        }
        if(slopes[3] > 0 && slopes[2] > 0 && slopes[1] > 0){
            return [1,0]
        }else if(slopes[3] < 0 && slopes[2] < 0 && slopes[1] < 0){
            return [0,1]
        }else{
            return [0,0]
        }
        
    }

    function genRegressionLine(_data,nRange){
        var yVal = [];
        for(var i = _data.length-nRange ; i < _data.length ; i++ ){
            yVal.push(_data[i]);
        }
        const xVal = Array(nRange ).fill().map((_, idx) => 1 + idx)
      
        const mX = xVal.reduce((a,v,i)=>(a*i+v)/(i+1));
        const mY = yVal.reduce((a,v,i)=>(a*i+v)/(i+1));

        let xValMinusMx = xVal.map(function(val){
            return  (val - mX)
        })

        let xValMinusMxSquare = xValMinusMx.map(function(val){
            return  val*val
        })

        let yValMinusMy = yVal.map(function(val){
            return  (val - mY)
        })
      
        let diffMxTimediffMy = yValMinusMy.map(function(val,index){
            return val * xValMinusMx[index]
        })

        const sumSquareError = xValMinusMxSquare.reduce((a, b) => a + b, 0)

        const sumdiffMxTimediffMy = diffMxTimediffMy.reduce((a, b) => a + b, 0)
        
        let slope = sumdiffMxTimediffMy/sumSquareError

        let constantC = mY - mX*slope

        return [slope,constantC]
    }

    function getCoord(arr,startX,endX,nRage){
        let startY = 1 * arr[0] + arr[1]
        let endY = nRage * arr[0] + arr[1]
        return [[startX,startY],[endX,endY]]
    }

    function isUpTrend(slope,_data,sma100,nRange,slopeSpec){
        let tmp = [
                {
                name: {
                    slope: 'Slope: ' + slope
                },
                value: sma100[_data.length-1],
                xAxis: _data.length-1,
                yAxis: sma100[_data.length-1],
                color: "#000",
            }
        ]
        var allSMA100Low = true;
        for(var i = _data.length-nRange ; i < _data.length ; i++ ){
            if(sma100[i] > _data[i][2]){
                allSMA100Low = false
                return [tmp, false]
            }        
        }
        if(allSMA100Low == true && slope > slopeSpec){
            return [tmp, true]
        }else{
            return [tmp, false]
        }
    }

    function sma100ArrowBelow(_data,sma100,nRange){
        for(var i = _data.length-nRange ; i < _data.length ; i++ ){
            if(sma100[i] > _data[i][2]){
                return false
            }        
        }
        return true;
    }

    function sma100PresentBelow(_data,sma100){
        c = _data.length-1
        if(sma100[c] > _data[c][2]){
            return false
        }   

        return true;
    }

    function sma100ArrowAbove(_data,sma100,nRange){   
        for(var i = _data.length-nRange ; i < _data.length ; i++ ){
            if(sma100[i] < _data[i][3]){
                return false
            }        
        }
        return true;
    }

    function sma100PresentAbove(_data,sma100){   
        c = _data.length-1
        if(sma100[c] < _data[c][3]){
            return false
        }   

        return true;
    }

    function getMomenttumBar(_data,presentLevel,gain){ 
        let present = _data[_data.length-1]
        let previous1 = _data[_data.length-2]
        let previous2 = _data[_data.length-3]
        let previous3 = _data[_data.length-4]  

    //     if(isCorrectWickTail(previous1,80) == false || isCorrectWickTail(previous2,80) == false || isCorrectWickTail(previous3,80) == false){
    //         return {
    //             id : present[4],
    //             foundBar : false,
    //             type : '',
    //         }
    //    }

        let diffHiLow_present = present[3] - present[2];
        let diffHiLow_previous1 = previous1[3]- previous1[2];
        let diffHiLow_previous2 = previous2[3] - previous2[2];
        let diffHiLow_previous3 = previous3[3] - previous3[2];

        if(diffHiLow_present > gain*(diffHiLow_previous1) && diffHiLow_present > gain*(diffHiLow_previous2) && diffHiLow_present > gain*(diffHiLow_previous3)){
            if(present[2] < previous1[2] && present[2] < previous2[2]  && present[2] < previous3[2] && presentLevel.sma100_present_above == true){
                return {
                    id : present[4],
                    foundBar : true,
                    type : 1,
                }
            } else if(present[2] > previous1[2] && present[2] > previous2[2]  && present[2] > previous3[2] && presentLevel.sma100_present_below == true){
                return {
                    id : present[4],
                    foundBar : true,
                    type : 2,
                }
            }else{
                return {
                    id : present[4],
                    foundBar : false,
                    type : '',
                }
            }
        }
        return {
            id : present[4],
            foundBar : false,
            type : '',
        }
    }

    function getTrendPattern(_data,presentLevel){
        let present = _data[_data.length-1]
        let previous1 = _data[_data.length-2]
        let previous2 = _data[_data.length-3]
        let previous3 = _data[_data.length-4]  

        if(isCorrectWickTail(previous1,30) == false || isCorrectWickTail(previous2,30) == false || isCorrectWickTail(previous3,30) == false){
            return {
                id : present[4],
                foundBar : false,
                type : '',
            }
       }

        if(presentLevel.sma100_present_below == true){ //check up trend
            if(previous1[0] > previous2[0] && previous2[0] > previous3[0] && previous1[2] > previous2[2] && previous2[2] > previous3[2] ){
                return {
                    id : present[4],
                    foundBar : true,
                    type : 2,
                }
            }else{
                return {
                    id : present[4],
                    foundBar : false,
                    type : '',
                }
            }
        }else if(presentLevel.sma100_present_above == true){ //check down trend
            if(previous1[0] < previous2[0] && previous2[0] < previous3[0] && previous1[2] < previous2[2] && previous2[2] < previous3[2] ){
                return {
                    id : present[4],
                    foundBar : true,
                    type : 1,
                }
            }else{
                return {
                    id : present[4],
                    foundBar : false,
                    type : '',
                }
            }
        }else{
            return {
                id : present[4],
                foundBar : false,
                type : '',
            }
        }

    }

    function isContinuityDownTrendrend(_data,sma100){
        let downtren0 = sma100[sma100.length-1] - _data[_data.length-1][3]
        let downtren1 = sma100[sma100.length-2] - _data[_data.length-2][3]
        let downtren2 = sma100[sma100.length-3] - _data[_data.length-3][3]  

        if(downtren0 > downtren1 && downtren1 > downtren2){
            return true
        }else {
            return false
        }
    }

    function twoBarsUp(_data,barSize){
        let presentbarsize = _data[_data.length-1][1] - _data[_data.length-1][0] 
        let previous1 = _data[_data.length-2][1] -_data[_data.length-2][0]
        let previous2 = _data[_data.length-3][1] - _data[_data.length-3][0]

        if(Math.abs(presentbarsize) > barSize && Math.abs(previous1) > barSize && Math.abs(previous2) > barSize && presentbarsize > 0 && previous1 > 0 && previous2 > 0){
            if(_data[_data.length-1][3] > _data[_data.length-2][3] && _data[_data.length-2][3] > _data[_data.length-3][3] &&  _data[_data.length-1][2] > _data[_data.length-2][2] && _data[_data.length-2][2] > _data[_data.length-3][2]){
                ////console.log('found two bar up')
                return true
            }else{
                return false 
            }
        }else{
            return false
        }
    }

    function bullishTrend(_data,barsize,gain,numbars){
        for (let i = 1 ; i <= numbars; i++){
            let open = _data[_data.length-i][0]
            let close = _data[_data.length-i][1]
            let body = close - open
            if(body < 0 || Math.abs(body) < barsize*gain){
                return false
            }
        }
        return true
    }

    function bullishLadder(_data,numbars){
        for (let i = 1 ; i < numbars; i++){
            let preopen = _data[_data.length-i][0]
            let postopen = _data[_data.length-i-1][0]

            let preclose = _data[_data.length-i][1]
            let postclose = _data[_data.length-i-1][1]

            if(preopen < postopen){
                return false
            }
            if(preclose < postclose){
                return false
            }
        }

        return true
    }

    

    function bullishMomentum(_data,barsize,_percent,_percentstd){
        let close = _data[_data.length-1][1]
        let open = _data[_data.length-1][0]
        
        let closeprevious = _data[_data.length-2][1]
        let openprevious = _data[_data.length-2][0]
        
        let body = close - open
        let previousbody = closeprevious - openprevious
        
        if(body < 0 || previousbody < 0 || body < previousbody ||  body < barsize ||  previousbody < barsize ){  
            return false
        }

        let percent = ((Math.abs(body) - Math.abs(previousbody))/Math.abs(previousbody))*100

        let percentstd = ((Math.abs(body) - Math.abs(barSize))/Math.abs(barSize))*100
     
        if(percent > _percent && percentstd > _percentstd){
            return true
        }else{
            return false
        }

    }

    function bearishTrend(_data,barsize,gain,numbars){
        for (let i = 1 ; i <= numbars; i++){
            let open = _data[_data.length-i][0]
            let close = _data[_data.length-i][1]
            let body = open - close 
            if(body < 0 || Math.abs(body) < barsize*gain){
                return false
            }
        }
        return true
    }

    function pipChange(fromPrice,toPrice,degit){
        let multipleNum = 10
        if (degit % 2 == 0){
            multipleNum = 1
        }
        // ////console.log('degit')
        return ((toPrice - fromPrice) * Math.pow(10, 1*degit))/multipleNum 
    }

    function pipPricePerLotsize(symbol,degit,currentPrice,contractSize,lotsize,usdbase){
        if(symbol.substring(0, 3) == 'USD'){
            return (((Math.pow(10, (-1)*degit))/currentPrice)*contractSize)*lotsize
        }
        else if(symbol.substring(3, 6) == 'USD'){
            return ((Math.pow(10, (-1)*degit))*contractSize)*lotsize
        }else{
            return (((Math.pow(10, (-1)*degit))/currentPrice)*contractSize)*lotsize*usdbase
        }
    }

    function stopLossPrice(percent,balance){
        return percent * balance
    }

    function getLotSize(stoplostPrice,numPips,pipPrice){
        return stoplostPrice/(numPips*pipPrice)
    }
    
    function bearishLadder(_data,numbars){
        for (let i = 1 ; i < numbars; i++){
            let preopen = _data[_data.length-i][0]
            let postopen = _data[_data.length-i-1][0]

            let preclose = _data[_data.length-i][1]
            let postclose = _data[_data.length-i-1][1]
       
            if(preopen > postopen){
                return false
            }
            if(preclose > postclose){
                return false
            }
        }
        return true
    }

    function threeBearishLadder(_data){
        let open0 = _data[_data.length-1][0]
        let close0 = _data[_data.length-1][1]
        let diff0 = open0 - close0

        let open1 = _data[_data.length-2][0]
        let close1 = _data[_data.length-2][1]
        let diff1 = open1 - close1

        let open2 = _data[_data.length-3][0]
        let close2 = _data[_data.length-3][1]
        let diff2 = open2 - close2

        if(open0 > open1 || open0 > open2 || open1 > open2 || close0 > close1 || close0 > close2 || close1 > close2){
            return false
        }else{
            if(Math.abs(diff0) > Math.abs(diff1) && Math.abs(diff1) > Math.abs(diff2)){
                return true
            }else{
                return false
            }            
        }
    }

    function threeBearishLadderBackTest(_data,stdbarsize,sma100){
        let open0 = _data[_data.length-2][0]
        let close0 = _data[_data.length-2][1]
        let high0 = _data[_data.length-2][3]
        let low0 = _data[_data.length-2][2]
        let diff0 = open0 - close0

        let open1 = _data[_data.length-3][0]
        let close1 = _data[_data.length-3][1]
        let high1 = _data[_data.length-3][3]
        let low1 = _data[_data.length-3][2]
        let diff1 = open1 - close1

        let open2 = _data[_data.length-4][0]
        let close2 = _data[_data.length-4][1]
        let high2 = _data[_data.length-4][3]
        let low2 = _data[_data.length-4][2]
        let diff2 = open2 - close2

        // if(high0 > high1 || high0 > high2 || high1 > high2 || low0 > low1 || low0 > low2 || low1 > low2 || Math.abs(diff0) < stdbarsize || Math.abs(diff0) < (0.5*stdbarsize) || diff0 < 0 || diff1 < 0 || diff2 < 0){
        if(high0 > high1 || high0 > high2 || high1 > high2 || low0 > low1 || low0 > low2 || low1 > low2 || Math.abs(diff0) < stdbarsize || Math.abs(diff0) < (0.5*stdbarsize) || high2 > sma100){
            return false
        }else{
            //console.log(_data[_data.length-2])
            return true
            // if(Math.abs(diff0) > Math.abs(diff1) && Math.abs(diff1) > Math.abs(diff2)){
            //     return true
            // }else{
            //     return false
            // }            
        }
    }

    function threeBullishLadderBackTest(_data,stdbarsize,sma100){
        let open0 = _data[_data.length-2][0]
        let close0 = _data[_data.length-2][1]
        let high0 = _data[_data.length-2][3]
        let low0 = _data[_data.length-2][2]
        let diff0 = open0 - close0

        let open1 = _data[_data.length-3][0]
        let close1 = _data[_data.length-3][1]
        let high1 = _data[_data.length-3][3]
        let low1 = _data[_data.length-3][2]
        let diff1 = open1 - close1

        let open2 = _data[_data.length-4][0]
        let close2 = _data[_data.length-4][1]
        let high2 = _data[_data.length-4][3]
        let low2 = _data[_data.length-4][2]
        let diff2 = open2 - close2

        // console.log()

        // if(high0 < high1 || high0 < high2 || high1 < high2 || low0 < low1 || low0 < low1 || low1 < low2 || Math.abs(diff0) < stdbarsize || Math.abs(diff0) < (0.5*stdbarsize) || diff0 > 0 || diff1 > 0 || diff2 > 0){
        if(high0 < high1 || high0 < high2 || high1 < high2 || low0 < low1 || low0 < low2 || low1 < low2 || Math.abs(diff0) < stdbarsize || Math.abs(diff0) < (0.5*stdbarsize) || low2 < sma100){
            return false
        }else{
            // if(Math.abs(diff0) > Math.abs(diff1) && Math.abs(diff1) > Math.abs(diff2)){
            //     return true
            // }else{
            //     return false
            // } 
            // //console.log(_data[_data.length-2])
            return true           
        }
    }

    function threeBullishLadder(_data){
        let open0 = _data[_data.length-1][0]
        let close0 = _data[_data.length-1][1]
        let diff0 = open0 - close0

        let open1 = _data[_data.length-2][0]
        let close1 = _data[_data.length-2][1]
        let diff1 = open1 - close1

        let open2 = _data[_data.length-3][0]
        let close2 = _data[_data.length-3][1]
        let diff2 = open2 - close2

        if(open0 < open1 || open0 < open2 || open1 < open2 || close0 < close1 || close0 < close2 || close1 < close2){
            return false
        }else{
            if(Math.abs(diff0) > Math.abs(diff1) && Math.abs(diff1) > Math.abs(diff2)){
                return true
            }else{
                return false
            }            
        }
    }

    function bearishCurve(_data){
        // //console.log(_data)
        let m1_open = _data[0][0]
        let m1_close = _data[0][1]
        let m5_open = _data[1][0]
        let m5_close = _data[1][1]
        let m15_open = _data[2][0]
        let m15_close = _data[2][1]
        let m30_open = _data[3][0]
        let m30_close = _data[3][1]
        // let h1_open = _data[4][0]
        // let h1_close = _data[4][1]

        if(m1_close > m1_open || m5_close > m5_open || m15_close > m15_open || m30_close > m30_open){
            return false
        }else{
            
            if(m1_open < m5_open && m5_open < m15_open && m15_open < m30_open){
                return true
            }else{
                return false
            }
        }
    }
    function bullishCurve(_data){
        let m1_open = _data[0][0]
        let m1_close = _data[0][1]
        let m5_open = _data[1][0]
        let m5_close = _data[1][1]
        let m15_open = _data[2][0]
        let m15_close = _data[2][1]
        let m30_open = _data[3][0]
        let m30_close = _data[3][1]
        // let h1_open = _data[4][0]
        // let h1_close = _data[4][1]
    
        if(m1_close < m1_open || m5_close < m5_open || m15_close < m15_open || m30_close < m30_open ){
            return false
        }else{
            if(m1_open > m5_open && m5_open > m15_open && m15_open > m30_open){
                return true
               
            }else{
                return false
            }
        }
    }

    function bearishMomentum(_data,barsize,_percent,_percentstd){
        let close = _data[_data.length-1][1]
        let open = _data[_data.length-1][0]
        
        let closeprevious = _data[_data.length-2][1]
        let openprevious = _data[_data.length-2][0]
        
        let body = close - open

        
        let previousbody = closeprevious - openprevious
        
        if(body > 0 || previousbody > 0 || Math.abs(body) < Math.abs(previousbody) ||  Math.abs(body) < barsize ||  Math.abs(previousbody) < barsize ){  
            return false
        }

        let percent = ((Math.abs(body) - Math.abs(previousbody))/Math.abs(previousbody))*100

        let percentstd = ((Math.abs(body) - Math.abs(barSize))/Math.abs(barSize))*100
     
        if(percent > _percent && percentstd > _percentstd){
            return true
        }else{
            return false
        }


        // let open = _data[_data.length-1][0]
        // let close = _data[_data.length-1][1]
        // let body = open - close

        // if(body < 0  || Math.abs(body) < barsize*upgain){
        //     return false
        // }
        // for (let i = 1 ; i <= numbars; i++){
        //     let open = _data[_data.length-i-1][0]
        //     let close = _data[_data.length-i-1][1]
        //     let body = close - open
  
        //     if(Math.abs(body) > barsize*downgain){
        //         return false
        //     }
        // }
        // return true
    }

    function bullishBig(_data,barsize,gain){
        let open = _data[_data.length-1][0]
        let close = _data[_data.length-1][1]
        let body = close - open 

        if(body < barsize*gain){
            return false
        }
        return true
    }


    function bearishBig(_data,barsize,gain){
        let open = _data[_data.length-1][0]
        let close = _data[_data.length-1][1]
        let body = open - close 

        if(body < barsize*gain){
            return false
        }
        return true
    }

    function shootingStar(_data,barsize,downgain,percentwick,percenttail){
        let open = _data[_data.length-1][0]
        let close = _data[_data.length-1][1]
        let body = open - close

        let diffbodywick = 0;
        let diffbodytail = 0;
     
        if(body < 0 ){

            return false
        }
        
        let openSubtractClose = _data[_data.length-2][0] - _data[_data.length-2][1]
        let bodysize = Math.abs(openSubtractClose)
        if(openSubtractClose > 0){
            let wick = _data[_data.length-2][3] - _data[_data.length-2][0]
            diffbodywick = 100-((Math.abs(openSubtractClose) - Math.abs(wick))*100/Math.abs(openSubtractClose))
            let tail = _data[_data.length-2][2] - _data[_data.length-2][1]
            diffbodytail = 100-((Math.abs(openSubtractClose) - Math.abs(tail))*100/Math.abs(openSubtractClose))
        }else{
            let wick = _data[_data.length-2][3] - _data[_data.length-2][1]
            diffbodywick = 100-((Math.abs(openSubtractClose) - Math.abs(wick))*100/Math.abs(openSubtractClose))

            let tail = _data[_data.length-2][2] - _data[_data.length-2][0]
            diffbodytail = 100-((Math.abs(openSubtractClose) - Math.abs(tail))*100/Math.abs(openSubtractClose))
            // 
        }
        if(diffbodywick > percentwick && diffbodytail < percenttail && bodysize > barsize*downgain){
            return true
        }else{
            return false
        }

    }

    function uptrendPinbar(_data,stdbarsize,digit,pipdistant,sma100){
        // let openSubtractClose_confirm = _data[_data.length-2][0] - _data[_data.length-2][1]
        let openSubtractClose_key = _data[_data.length-2][0] - _data[_data.length-2][1]

        let highLowSize_key = _data[_data.length-2][3] - _data[_data.length-2][2]
        if(highLowSize_key > stdbarsize*2 ){
            if(openSubtractClose_key<0){
                let wick = _data[_data.length-2][3] - _data[_data.length-2][1]
                diffbodywick_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(wick))*100/Math.abs(openSubtractClose_key))  

                let tail = _data[_data.length-2][0] - _data[_data.length-2][2]
                diffbodytail_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(tail))*100/Math.abs(openSubtractClose_key))          
            }else{
                
                let wick = _data[_data.length-2][3] - _data[_data.length-2][0]
                diffbodywick_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(wick))*100/Math.abs(openSubtractClose_key)) 

                let tail = _data[_data.length-2][1] - _data[_data.length-2][2]
                diffbodytail_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(tail))*100/Math.abs(openSubtractClose_key))
            }
          
            if(diffbodytail_key >= 250 && diffbodytail_key > 3*diffbodywick_key){
                // //console.log('diffbodywick:' + diffbodywick_key)
                // //console.log('diffbodytail:'+diffbodytail_key)
                
                // if (openSubtractClose_confirm <= 0){
                //     if(_data[_data.length-3][2] > sma100){
                //         return true
                //     }else{
                //         return false
                //     }
                    
                // }else{
                //     return false
                // }
                return true
            }else{
                return false
            }
        }else{
            return false
        }
    }

    function downtrendPinbar(_data,stdbarsize,digit,pipdistant,sma100){
        // let openSubtractClose_confirm = _data[_data.length-2][0] - _data[_data.length-2][1]
        let openSubtractClose_key = _data[_data.length-2][0] - _data[_data.length-2][1]
        let highLowSize_key = _data[_data.length-2][3] - _data[_data.length-2][2]
        if(highLowSize_key > stdbarsize*2 ){
            if(openSubtractClose_key < 0){ //green
                let wick = _data[_data.length-2][3] - _data[_data.length-2][1]
                diffbodywick_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(wick))*100/Math.abs(openSubtractClose_key))  

                let tail = _data[_data.length-2][0] - _data[_data.length-2][2]
                diffbodytail_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(tail))*100/Math.abs(openSubtractClose_key))   
            }else{
                let wick = _data[_data.length-2][3] - _data[_data.length-2][0]
                diffbodywick_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(wick))*100/Math.abs(openSubtractClose_key)) 

                let tail = _data[_data.length-2][1] - _data[_data.length-2][2]
                diffbodytail_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(tail))*100/Math.abs(openSubtractClose_key))
            }

            if(diffbodywick_key >= 250 && diffbodywick_key > 3*diffbodytail_key){
                // //console.log('diffbodywick:' + diffbodywick_key)
                // //console.log('diffbodytail:'+diffbodytail_key)
                
                // if (openSubtractClose_confirm >= 0){
                //     if(_data[_data.length-3][3] < sma100){
                //         return true
                //     }else{
                //         return false
                //     }
                // }else{
                //     return false
                // }
                return true
            }else{
                return false
            }

        }else{
            return false
        }
    }

    function DoublePinbar(_data,stdbarsize,slope,sma100,digit,pipdistant){
        if(slope<0){
            let diffbodytail_key =0;
            let diffbodywick_key =0;
            let openSubtractClose_key = _data[_data.length-2][0] - _data[_data.length-2][1]
            let highLowSize_key = _data[_data.length-2][3] - _data[_data.length-2][2]

            let openSubtractClose_brother = _data[_data.length-3][0] - _data[_data.length-3][1]
            let highLowSize_brother = _data[_data.length-3][3] - _data[_data.length-3][2]

           
            
            if(highLowSize_key < stdbarsize*2 || highLowSize_brother < stdbarsize*2 ){
                return [0,0]
            }else{
                // //console.log('-----------')
                // //console.log('sdt15: ' + stdbarsize*2)
                
                // //console.log('highLowSize: ' +highLowSize_key)
                // //console.log('-----------')
                if(openSubtractClose_key<0){
                    let wick = _data[_data.length-2][3] - _data[_data.length-2][1]
                    diffbodywick_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(wick))*100/Math.abs(openSubtractClose_key))  

                    let tail = _data[_data.length-2][0] - _data[_data.length-2][2]
                    diffbodytail_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(tail))*100/Math.abs(openSubtractClose_key))          
                }else{
                    
                    let wick = _data[_data.length-2][3] - _data[_data.length-2][0]
                    diffbodywick_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(wick))*100/Math.abs(openSubtractClose_key)) 

                    let tail = _data[_data.length-2][1] - _data[_data.length-2][2]
                    diffbodytail_key = 100-((Math.abs(openSubtractClose_key) - Math.abs(tail))*100/Math.abs(openSubtractClose_key))
                }

                let pipchange= pipChange(parseFloat(_data[_data.length-2][3]),parseFloat(sma100),digit)

                if(diffbodywick_key >= 250 && diffbodywick_key > 3*diffbodytail_key){
                    
                    if(pipchange > pipdistant){
                        //console.log('pip change' + pipchange)
                        return [1,0]
                    }else{
                        return [0,0]
                    }
                    
                }else{
                    return [0,0]
                }
            }

        }else{
            return [0,0]
        }
    }

    function PinBar(_data,stdbarsize,slope,sma100,digit){
        // //console.log(stdbarsize)
        let diffbodytail =0;
        let diffbodywick =0;
        let openSubtractClose = _data[_data.length-2][0] - _data[_data.length-2][1]
        let highLowSize = _data[_data.length-2][3] - _data[_data.length-2][2]
        if(highLowSize < stdbarsize*2 ){
            // //console.log('less than stdbar size')
            return [0,0]
        }
        if(slope<0){
            if(openSubtractClose<0){
                let wick = _data[_data.length-2][3] - _data[_data.length-2][1]
                diffbodywick = 100-((Math.abs(openSubtractClose) - Math.abs(wick))*100/Math.abs(openSubtractClose))          
                
                let tail = _data[_data.length-2][0] - _data[_data.length-2][2]
                diffbodytail = 100-((Math.abs(openSubtractClose) - Math.abs(tail))*100/Math.abs(openSubtractClose))  
            }else{
                
                let wick = _data[_data.length-2][3] - _data[_data.length-2][0]
                diffbodywick = 100-((Math.abs(openSubtractClose) - Math.abs(wick))*100/Math.abs(openSubtractClose))
            
                let tail = _data[_data.length-2][1] - _data[_data.length-2][2]
                diffbodytail = 100-((Math.abs(openSubtractClose) - Math.abs(tail))*100/Math.abs(openSubtractClose))
            }

           

            if(diffbodywick >= 250 && diffbodywick > 3*diffbodytail){
                let keybodySize = Math.abs(_data[_data.length-2][0] - _data[_data.length-2][1]) 
                let brotherSize = Math.abs(_data[_data.length-3][0] - _data[_data.length-3][1])
                let littleBrotherSize = Math.abs(_data[_data.length-4][0] - _data[_data.length-4][1])
                if(littleBrotherSize > stdbarsize && littleBrotherSize > brotherSize &&  littleBrotherSize > keybodySize){
                    // //console.log('little brother bigger than std')
                    let openkey = _data[_data.length-2][0]
                    let closekey = _data[_data.length-2][1]


                    let openbrother = _data[_data.length-3][0]
                    let closebrother = _data[_data.length-3][1]
                   
                    let openlittlebrother = _data[_data.length-4][0]
                    let closelittlebrother = _data[_data.length-4][1]

                    if(openkey > openbrother && openbrother > openlittlebrother && closekey > closebrother && closebrother > closelittlebrother){
                        // //console.log('little brother bigger than std and ladder')
                        let pipchange= pipChange(parseFloat(_data[_data.length-2][3]),parseFloat(sma100),digit)
                        // //console.log(pipchange)
                        if(pipchange > 4 ){
                        
                            return [1,0]
                        }else{
                            return [0,0]  
                        }
                    }else{
                        return [0,0]
                    }
                }else{
                    return [0,0]
                }
            }else{
                return [0,0]
            }
       

        }else{
            if(openSubtractClose<0){
                let tail = _data[_data.length-2][0] - _data[_data.length-2][2]
                diffbodytail = 100-((Math.abs(openSubtractClose) - Math.abs(tail))*100/Math.abs(openSubtractClose))          
            
            }else{
                
                let tail = _data[_data.length-2][1] - _data[_data.length-2][2]
                diffbodytail = 100-((Math.abs(openSubtractClose) - Math.abs(tail))*100/Math.abs(openSubtractClose))
              
            }
            if(isFinite(diffbodytail) == false){
                return [0,0]
            }
            // //console.log(diffbodytail) 
            // //console.log('-----') 
            // //console.log(isFinite(diffbodytail)) 
            if(diffbodytail >= 250){
                let keybodySize = Math.abs(_data[_data.length-2][0] - _data[_data.length-2][1]) 
                let brotherSize = Math.abs(_data[_data.length-3][0] - _data[_data.length-3][1])
                let littleBrotherSize = Math.abs(_data[_data.length-4][0] - _data[_data.length-4][1])
                if(littleBrotherSize > stdbarsize && littleBrotherSize > brotherSize &&  littleBrotherSize > keybodySize){
                    // //console.log('little brother bigger than std')
                    let openkey = _data[_data.length-2][0]
                    let closekey = _data[_data.length-2][1]


                    let openbrother = _data[_data.length-3][0]
                    let closebrother = _data[_data.length-3][1]
                   
            
                    let openlittlebrother = _data[_data.length-4][0]
                    let closelittlebrother = _data[_data.length-4][1]

                    if(openkey < openbrother && openbrother < openlittlebrother && closekey < closebrother && closebrother < closelittlebrother){
                        // //console.log('little brother bigger than std and ladder')
                        let pipchange= pipChange(parseFloat(sma100),parseFloat(_data[_data.length-2][3]),digit)
                        // //console.log(pipchange)
                        if(pipchange > 4 ){
                            // //console.log(slope)
                            //console.log('little brother bigger than std and ladder and 7 pip away')
                            return [0,1]
                        }else{
                            return [0,0]  
                        }
                    }else{
                        return [0,0]
                    }

                }else{
                    return [0,0]
                }
            }else{
                return [0,0]
            }
        }
    }

    function hammer(_data,barsize,downgain,percentwick,percenttail){
        let open = _data[_data.length-1][0]
        let close = _data[_data.length-1][1]
        let body =  close - open

        let diffbodywick = 0;
        let diffbodytail = 0;
     
        if(body < 0 ){

            return false
        }
        
        let openSubtractClose = _data[_data.length-2][1] - _data[_data.length-2][0]
        let bodysize = Math.abs(openSubtractClose)
        if(openSubtractClose < 0){
            let wick = _data[_data.length-2][3] - _data[_data.length-2][0]
            diffbodywick = 100-((Math.abs(openSubtractClose) - Math.abs(wick))*100/Math.abs(openSubtractClose))
            let tail = _data[_data.length-2][2] - _data[_data.length-2][1]
            diffbodytail = 100-((Math.abs(openSubtractClose) - Math.abs(tail))*100/Math.abs(openSubtractClose))
        }else{
            let wick = _data[_data.length-2][3] - _data[_data.length-2][1]
            diffbodywick = 100-((Math.abs(openSubtractClose) - Math.abs(wick))*100/Math.abs(openSubtractClose))

            let tail = _data[_data.length-2][2] - _data[_data.length-2][0]
            diffbodytail = 100-((Math.abs(openSubtractClose) - Math.abs(tail))*100/Math.abs(openSubtractClose))
        }
        if(diffbodywick < percentwick && diffbodytail > percenttail && bodysize > barsize*downgain){
            return true
        }else{
            return false
        }

    }

    function twoBarsDown(_data,barSize){
        let presentbarsize = _data[_data.length-1][0] - _data[_data.length-1][1]
        let previous1 = _data[_data.length-2][0] - _data[_data.length-2][1]
        let previous2 = _data[_data.length-3][0] - _data[_data.length-3][1]

        if(Math.abs(presentbarsize) > barSize && Math.abs(previous1) > barSize && Math.abs(previous2) > barSize && presentbarsize > 0 && previous1 > 0 && previous2 > 0){
            if(_data[_data.length-1][3] < _data[_data.length-2][3] && _data[_data.length-2][3] < _data[_data.length-3][3] &&  _data[_data.length-1][2] < _data[_data.length-2][2] && _data[_data.length-2][2] < _data[_data.length-3][2]){
                ////console.log('found two bar down')
                return true
            }else{
                return false 
            }
        }else{
            return false
        }

    }

    function momentumBarUp(_data,_barSize,barSizeRatio,gain){
        let barSize = _barSize*barSizeRatio
        let presentbarsize = _data[_data.length-1][0] - _data[_data.length-1][1]
        let previous1 = _data[_data.length-2][0] - _data[_data.length-2][1]
        let previous2 = _data[_data.length-3][0] - _data[_data.length-3][1]
        let positive = _data[_data.length-1][1] - _data[_data.length-2][1] 

        if(Math.abs(previous1) > barSize && Math.abs(previous2) > barSize && Math.abs(presentbarsize) > gain*Math.abs(previous1) && Math.abs(presentbarsize) > gain*Math.abs(previous2) && positive > 0 ){
            let diffbody_previouswick_1 = 0
            let diffbodytail_1 = 0
            let diffbody_previouswick_2 = 0
            let diffbodytail_2 = 0
            if(previous1 < 0){
                let previouswick_1 = _data[_data.length-2][3] -  _data[_data.length-2][1]
                diffbody_previouswick_1 = 100-((Math.abs(previous1) - Math.abs(previouswick_1))*100/Math.abs(previous1))
                let previoustail_1 = _data[_data.length-2][2] -  _data[_data.length-2][0]
                diffbodytail_1 = 100-((Math.abs(previous1) - Math.abs(previoustail_1))*100/Math.abs(previous1))
                
            }else{
                let previouswick_1 = _data[_data.length-2][3] -  _data[_data.length-2][0]
                diffbody_previouswick_1 = 100-((Math.abs(previous1) - Math.abs(previouswick_1))*100/Math.abs(previous1))
                let previoustail_1 = _data[_data.length-2][2] -  _data[_data.length-2][1]
                diffbodytail_1 = 100-((Math.abs(previous1) - Math.abs(previoustail_1))*100/Math.abs(previous1))
               
            }

            if(previous2 < 0){
                let previouswick_2 = _data[_data.length-3][3] -  _data[_data.length-3][1]
                diffbody_previouswick_2 = 100-((Math.abs(previous2) - Math.abs(previouswick_2))*100/Math.abs(previous2))
    
                let previoustail_2 = _data[_data.length-3][2] -  _data[_data.length-3][0]
                diffbodytail_2 = 100-((Math.abs(previous2) - Math.abs(previoustail_2))*100/Math.abs(previous2))
             
            }else{
                let previouswick_2 = _data[_data.length-3][3] -  _data[_data.length-3][0]
                diffbody_previouswick_2 = 100-((Math.abs(previous2) - Math.abs(previouswick_2))*100/Math.abs(previous2))
    
                let previoustail_2 = _data[_data.length-3][2] -  _data[_data.length-3][1]
                diffbodytail_2 = 100-((Math.abs(previous2) - Math.abs(previoustail_2))*100/Math.abs(previous2))
            }
            
            if(diffbody_previouswick_1 < 150 && diffbodytail_1 < 150 && diffbody_previouswick_2 < 150 && diffbodytail_2 < 150){
                ////console.log('found bullish engulfing 555')
                return true
            }else{
                return false
            }
            
        }else{
            return false
        }

    }

    function momentumBarDown(_data,_barSize,barSizeRatio,gain){
        let barSize = _barSize*barSizeRatio
        let presentbarsize = _data[_data.length-1][0] - _data[_data.length-1][1]
        let previous1 = _data[_data.length-2][0] - _data[_data.length-2][1]
        let previous2 = _data[_data.length-3][0] - _data[_data.length-3][1]
        let negative = _data[_data.length-1][1] - _data[_data.length-2][1] 

        if(Math.abs(previous1) > barSize && Math.abs(previous2) > barSize && Math.abs(presentbarsize) > gain*Math.abs(previous1) && Math.abs(presentbarsize) > gain*Math.abs(previous2) && negative < 0){
            ////console.log('bearish engulfing')
            return true
        }else{
            return false
        }
    }


    function isContinuityDownTrend(_data,sma100,trend){
        let uptren0 = _data[_data.length-1][2] -  sma100[sma100.length-1] 
        let uptren1 = _data[_data.length-2][2] - sma100[sma100.length-2]
        let uptren2 = _data[_data.length-3][2]  - sma100[sma100.length-3]   

        if(uptren0 > uptren1 && uptren1 > uptren2){
            return true
        }else {
            return false
        }
    }

    function bullishAllTimeframe(_data){
        if(parseFloat(_data[0].h1.close) > parseFloat(_data[0].h1.open)
            && parseFloat(_data[1].m30.close) > parseFloat(_data[1].m30.open)
            && parseFloat(_data[2].m15.close) > parseFloat(_data[2].m15.open)
            && parseFloat(_data[3].m5.close) > parseFloat(_data[3].m5.open) 
        ){
            return true
        }else{
            return false
        }
    }

    function bearishAllTimeframe(_data){
        if(parseFloat(_data[0].h1.close) < parseFloat(_data[0].h1.open)
            && parseFloat(_data[1].m30.close) < parseFloat(_data[1].m30.open)
            && parseFloat(_data[2].m15.close) < parseFloat(_data[2].m15.open)
            && parseFloat(_data[3].m5.close) < parseFloat(_data[3].m5.open) 
        ){
            return true
        }else{
            return false
        }
    }

    function isCorrectWickTail(data,percent){
        presentarr = data.filter((ohlc,idx) => idx < 4)
        let sorted = sortArr(presentarr);
        let body = sorted[2]-sorted[1]
        let wick = sorted[3]-sorted[2]
        let tail = sorted[1]-sorted[0]
        
        let diffbodywick = 100-((body - wick)*100/body)
        let diffbodytail = 100-((body - tail)*100/body)

        if (diffbodywick <= percent && diffbodytail <= percent) {
            
            return true;
        }
        return false;
    }

    function sortArr(numArray){
        numArray.sort(function(a, b) {
        return a - b;
        });
        return numArray;
    }

    function getSsma3LineOrder(ssma5,ssma8,ssma13){
        // isSsmaSequencing = isSssmaSequence(Smoth_SSMA5Arr,Smoth_SSMA8Arr,Smoth_SSMA13Arr)
        let isUpTrend = false;
        let isDownTrend = false;
        if((ssma5[ssma5.length-1] > ssma8[ssma8.length-1]) && (ssma8[ssma8.length-1] > ssma13[ssma13.length-1])){
            isUpTrend = true
        }

        if((ssma5[ssma5.length-1] < ssma8[ssma8.length-1]) && (ssma8[ssma8.length-1] < ssma13[ssma13.length-1])){
            isDownTrend = true
        }
        return {'aligator_order_uptrend': isUpTrend, 'aligator_order_downtrend': isDownTrend}
    }

    function StandardDeviationCalc(_array,nRange) {
        let array = _array.slice((_array.length - nRange), _array.length)
        const mean = array.reduce((a, b) => a + b) / nRange
        return Math.sqrt(array.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / nRange)
    }

    function RS(mArray,mRange) {
        var _closePriceChanged = [];
        var _closePriceChangedGain = [];
        var _closePriceChangedLost = [];
        var _avgGain = [];
        var _avgLost = [];
        
        var _RS = [];
        for (var i = 1; i < mArray.length; i++) {
            var closePriceChanged  = mArray[i] - mArray[i-1];
            _closePriceChanged.push(closePriceChanged);
            if(closePriceChanged > 0){
                _closePriceChangedGain.push(closePriceChanged);
                _closePriceChangedLost.push(0);
            }else{
                _closePriceChangedGain.push(0);
                _closePriceChangedLost.push(closePriceChanged*-1)
            }
        }

        var avgGain = _closePriceChangedGain.slice(0, mRange).reduce((a,c) => a + c, 0) / mRange;
        var avgLost = _closePriceChangedLost.slice(0, mRange).reduce((a,c) => a + c, 0) / mRange;

        _avgGain = [avgGain];
        _avgLost = [avgLost];


        for (var i = mRange; i < _closePriceChangedGain.length; i++) {
            _avgGain.push((_avgGain[i-mRange]*(mRange-1) + _closePriceChangedGain[i])/mRange );
        }

        for (var i = mRange; i < _closePriceChangedLost.length; i++) {
            _avgLost.push((_avgLost[i-mRange]*(mRange-1) + _closePriceChangedLost[i])/mRange );
        }
        for (var i = 0; i < _avgGain.length; i++) {
            var rs = _avgGain[i] / _avgLost[i];
            if(_avgLost[i] == 0){
                _RS.push(100);
            }else{
                _RS.push(100-(100/(1+rs)));
            }
        }
        return _RS;
    }

    function addCandleStick(){
        let candleSticks = [
            {
                'open' : 0.90725,
                'close' : 0.90723,
                'low' : 0.90713,
                'high' : 0.90742,
            },
            {
                'open' : 0.90724,
                'close' : 0.90726,
                'low' : 0.90713,
                'high' : 0.90732,
            },
            {
                'open' : 0.90725,
                'close' : 0.90737,
                'low' : 0.90719,
                'high' : 0.90742,
            },
            {
                'open' : 0.90735,
                'close' : 0.90717,
                'low' : 0.90717,
                'high' : 0.90745,
            },
            {
                'open' : 0.90717,
                'close' : 0.90715,
                'low' : 0.90711,
                'high' : 0.90724,
            }
        ]

        candleSticks.forEach(candle => {
            ////console.log(candle.open)
        });
        // let m15body = _arr1[0] -  _arr1[1]
        return []
    }

