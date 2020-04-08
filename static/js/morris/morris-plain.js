var Script = function() {

    function getResultFromEndpoint(endpoint, callback) {
        const host = 'http://127.0.0.1:5000';
        $.ajax(
            {
                type: 'GET',
                url: host + endpoint,
                dataType: 'json',
                success: callback,
                error: function (x, e) {
                    console.log('ERROR. endpoint: ' + endpoint 
                            + ', status: ' + x.status 
                            + ', response: ' + x.responsetext
                            + ', error: ' + e)
                }
            }
        );
    }

    getResultFromEndpoint('/casesCDF', function(cdfglobal) {
        var cdfglobaldata = [];
        for (let [key, value] of Object.entries(cdfglobal)) {
            var keyVal = parseFloat(key);
            keyVal = keyVal.toFixed(2);
            cdfglobaldata.push({'Cases': keyVal, 'CDF': value});
        }
        Morris.Line({
            element: 'cdf-global',
            data: cdfglobaldata,
            xkey: 'Cases',
            ykeys: ['CDF'],
            labels: ['CDF'],
            parseTime: false,
            xLabelAngle: 90,
            lineColors: ['#ffeb3b']
        });
    });

    getResultFromEndpoint('/casesCountryCDF/Greece', function(cdfGR) {
        var cdfGRdata = [];
        for (let [key, value] of Object.entries(cdfGR)) {
            var keyVal = parseFloat(key);
            keyVal = keyVal.toFixed(2);
            cdfGRdata.push({'Cases': keyVal, 'CDF': value});
        }
        Morris.Line({
            element: 'cdf-greece',
            data: cdfGRdata,
            xkey: 'Cases',
            ykeys: ['CDF'],
            labels: ['CDF'],
            parseTime: false,
            xLabelAngle: 90,
            lineColors: ['#f57f17']
        });
    });

    getResultFromEndpoint('/casesODDS', function(oddsglobal) {
        var oddsglobaldata = [];
        for (let [key, value] of Object.entries(oddsglobal)) {
            var keyVal = parseFloat(key);
            keyVal = keyVal.toFixed(2);
            oddsglobaldata.push({'Cases': keyVal, 'ODDS': Math.log10(value+1)});
        }
        Morris.Line({
            element: 'pdf-global',
            data: oddsglobaldata,
            xkey: 'Cases',
            ykeys: ['ODDS'],
            labels: ['ODDS'],
            parseTime: false,
            xLabelAngle: 90,
            lineColors: ['#81c784']
        });
    });

    getResultFromEndpoint('/casesCountryODDS/Greece', function(oddsGR) {
        var oddsGRdata = [];
        for (let [key, value] of Object.entries(oddsGR)) {
            var keyVal = parseFloat(key);
            keyVal = keyVal.toFixed(2);
            oddsGRdata.push({'Cases': keyVal, 'ODDS': Math.log10(value+1)});
        }
        Morris.Line({
            element: 'pdf-greece',
            data: oddsGRdata,
            xkey: 'Cases',
            ykeys: ['ODDS'],
            labels: ['ODDS'],
            parseTime: false,
            xLabelAngle: 90,
            lineColors: ['#2e7d32']
        });
    });

    getResultFromEndpoint('/capita_and_cases_per_country', function(capitacases) {
        // console.log(humanfreeCountry);
        var capitacasesData = [];
        for (let [key, value] of Object.entries(capitacases)) {
            capitacasesData.push({
                'Country': key, 
                'Cases':Math.log(value[0]+1),
                'Corruption': Math.log(value[1]+1.1)});
        }
        Morris.Bar({
            element: 'cases-per-capita',
            data: capitacasesData,
            xkey: 'Country',
            ykeys: ['Cases', 'Corruption'],
            labels: ['Cases', 'Corruption'],
            // parseTime: false,
            xLabelAngle: 90,
            gridTextSize: 8,
            barColors: ['#33FF64','#FF336E' ]
        });
    });

    getResultFromEndpoint('/china_vs_EU', function(chinaeu) {
        var chinaeudata = [];
        for (let [key, value] of Object.entries(chinaeu)) {
            chinaeudata.push({'Date': key, 'EU Cases':value[0], 'CN Cases': value[1]});
        }
        Morris.Bar({
            element: 'china-eu',
            data: chinaeudata,
            xkey: 'Date',
            ykeys: ['EU Cases', 'CN Cases'],
            labels: ['EU Cases', 'CN Cases'],
            // parseTime: false,
            xLabelAngle: 90,
            gridTextSize: 8,
            barColors: ['#4733FF','#FF3352' ]
        });
    });

    getResultFromEndpoint('/human_freedom_per_country', function(humanfreeCountry) {
        var freedomCountry = [];
        for (let [key, value] of Object.entries(humanfreeCountry)) {
            freedomCountry.push({'Country': key, 'Cases':Math.log(value[0]+1), 'human_freedom': value[1]});
        }
        Morris.Bar({
            element: 'humanfreedomCountry',
            data: freedomCountry,
            xkey: 'Country',
            ykeys: ['Cases', 'human_freedom'],
            labels: ['Cases', 'human_freedom'],
            // parseTime: false,
            xLabelAngle: 90,
            gridTextSize: 8,
            barColors: ['#03a9f4', '#ffc107']
        });
    });

    // GLOBAL MAP
    getResultFromEndpoint('/mapped_results', function(mapped) {
        var markers = [];
        for (let [key, value] of Object.entries(mapped)) {
            markers.push({'Country': key, 'lat':value[0], 'lng':value[1],'Deaths':value[2],'Cases':value[3]});
        }

        var map = L.map('map',{
                    center: [52.940692, -3.290210],
                    zoom: 2});
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
        L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
                            maxZoom: 20,
	                        attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'}).addTo(map);

        var myURL = jQuery( 'script[src$="morris-plain.js"]' ).attr( 'src' ).replace( 'morris-plain.js', '' );

        var myIcon = L.icon({
          iconUrl: myURL + '/covid.png',
          iconRetinaUrl: myURL + '/covid.png',
          iconSize: [29, 24],
          iconAnchor: [9, 21],
          popupAnchor: [0, -14]
        });



        for ( var i=0; i < markers.length; ++i )
            {L.circle( [markers[i].lat, markers[i].lng], {color: '#05aaac',
                        fillColor: '#05aaac',
                        fillOpacity: 0.5,
                        radius: markers[i].Cases*15} )
                .bindPopup( "<strong> Country:</strong>"+markers[i].Country+"<br>"+"<strong>Deaths:</strong>"+
                markers[i].Deaths+"<br>"+"<strong>Cases:</strong>"+markers[i].Cases)
                .addTo( map );}
    });
}();

function compareCases() {
    document.getElementById('cases-per-day').innerHTML = "";
    const country1 = document.getElementById("selectField1").value;
    const country2 = document.getElementById("selectField2").value;

    var endpointCasesDay1 = '/totalCasesDay';
    if (country1 !== 'WORLD'){
        endpointCasesDay1 = '/casesPerSpecificCountry/' + country1;
    }

    var totalCasesDay2 = '/totalCasesDay';
    if (country2 !== 'WORLD'){
        endpointCasesDay2 = '/casesPerSpecificCountry/' + country2;
    }

    const host = 'http://127.0.0.1:5000';
    $.when(
        $.ajax({type: 'GET', url: host + endpointCasesDay1, dataType: 'json'}),
        $.ajax({type: 'GET', url: host + endpointCasesDay2, dataType: 'json'})
    ).then(function(d1, d2) {
        var totalCasesDay1 = d1[0];
        var totalCasesDay2 = d2[0];
        var datas = [];
        for (let [key, value] of Object.entries(totalCasesDay1)) {
            if (key in totalCasesDay2){
                datas.push({'Day': key, 'Cases1': Math.log(value+1), 'Cases2': Math.log(totalCasesDay2[key]+1)});
            }
            else {
                datas.push({'Day': key, 'Cases1': Math.log(value+1), 'Cases2': Math.log(1)});
            }

        }
        Morris.Line({
            element: 'cases-per-day',
            data: datas,
            xkey: 'Day',
            ykeys: ['Cases1', 'Cases2'],
            labels: ['Κρούσματα (' + country1 + ')', 'Κρούσματα (' + country2 + ')'],
            parseTime: false,
            xLabelAngle: 90,
            lineColors: ['#d32f2f', '#3498dB']
        });
    });
}

function compareDeaths() {
    document.getElementById('death-ratio').innerHTML = "";
    const country1 = document.getElementById("selectFieldDeath1").value;
    const country2 = document.getElementById("selectFieldDeath2").value;

    var endpointCasesDay1 = '/totalCasesDay';
    var endpointDeathsDay1 = '/totalDeathsDay';
    var endpointCasesDay2 = '/totalCasesDay';
    var endpointDeathsDay2 = '/totalDeathsDay';
    if (country1 !== 'WORLD') {
        endpointCasesDay1 = '/casesPerSpecificCountry/' + country1;
        endpointDeathsDay1 = '/deathsPerSpecificCountry/' + country1;
    }
    if (country2 !== 'WORLD') {
        endpointCasesDay2 = '/casesPerSpecificCountry/' + country2;
        endpointDeathsDay2 = '/deathsPerSpecificCountry/' + country2;
    }
        
    const host = 'http://127.0.0.1:5000';
    $.when(
        $.ajax({type: 'GET', url: host + endpointCasesDay1, dataType: 'json'}),
        $.ajax({type: 'GET', url: host + endpointDeathsDay1, dataType: 'json'}),
        $.ajax({type: 'GET', url: host + endpointCasesDay2, dataType: 'json'}),
        $.ajax({type: 'GET', url: host + endpointDeathsDay1, dataType: 'json'})
    ).then(function(d1, d2, d3, d4) {
        var totalCasesDay1 = d1[0];
        var totalDeathsDay1 = d2[0];
        var totalCasesDay2 = d3[0];
        var totalDeathsDay2 = d4[0];
        var deathsPerDay = [];
        var casesUpToNow1 = 0;
        var casesUpToNow2 = 0;
        var deathsUpToNow1 = 0;
        var deathsUpToNow2 = 0;
        for (let [key, value] of Object.entries(totalDeathsDay1)) {
            if (key in totalCasesDay1) {
                casesUpToNow1 += totalCasesDay1[key];
            }
            if (key in totalCasesDay2) {
                casesUpToNow2 += totalCasesDay2[key];
            }
            deathsUpToNow1 += value;
            if (key in totalDeathsDay2) {
                deathsUpToNow2 += totalDeathsDay2[key];
            }
            if (casesUpToNow1 === 0) {
                if (casesUpToNow2 === 0) {
                    deathsPerDay.push({'Day': key, 'Cases1': 0, 'Cases2': 0});
                } else {
                    deathsPerDay.push({
                        'Day': key,
                        'Cases1': 0,
                        'Cases2': (deathsUpToNow2 / casesUpToNow2 * 100).toFixed(2)
                    });
                }
            } else {
                if (casesUpToNow2 === 0) {
                    deathsPerDay.push({
                        'Day': key,
                        'Cases1': (deathsUpToNow1 / casesUpToNow1 * 100).toFixed(2),
                        'Cases2': 0
                    });
                } else {
                    deathsPerDay.push({
                        'Day': key,
                        'Cases1': (deathsUpToNow1 / casesUpToNow1 * 100).toFixed(2),
                        'Cases2': (deathsUpToNow2 / casesUpToNow2 * 100).toFixed(2)
                    });
                }
            }
        }
        console.log(casesUpToNow1);
        Morris.Line({
            element: 'death-ratio',
            data: deathsPerDay,
            xkey: 'Day',
            ykeys: ['Cases1', 'Cases2'],
            labels: ['Ποσοστό Θανάτων (' + country1 + ')', 'Ποσοστό Θανάτων (' + country2 + ')'],
            postUnits: ['%'],
            parseTime: false,
            xLabelAngle: 90,
            lineColors: ['#d32f2f', '#3498dB']
        });
    });

}
