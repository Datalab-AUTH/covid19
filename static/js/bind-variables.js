function getResultFromEndpoint(endpoint, callback) {
    const host = 'http://127.0.0.1:5000';
    $.ajax(
        {
            type: 'GET',
            url: host + endpoint,
            dataType: 'json',
            success: callback,
            error: function (x, e) {
                alert('server error occoured');
                if (x.status == 0) {
                    alert('0 error');
                } else if (x.status == 404) {
                    alert('404 error');
                } else if (x.status == 500) {
                    alert('500 error');
                } else if (e == 'parsererror') {
                    alert('Error.nParsing JSON Request failed.');
                } else if (e == 'timeout') {
                    alert('Time out.');
                } else {
                    alert(x.responseText);
                }
            }
        }
    );
}

function processRawData(allText) {
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');
    var lines = [];

    var table = document.getElementById('info-table-body');
    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        if (data.length === headers.length) {

            var row = document.createElement("tr");
            var country = document.createElement("td");
            country.textContent = data[0];
            var cases = document.createElement("td");
            cases.textContent = data[1];
            var deaths = document.createElement("td");
            deaths.textContent = data[2];

            row.appendChild(country);
            row.appendChild(cases);
            row.appendChild(deaths);

            table.appendChild(row);
        }
    }
}

getResultFromEndpoint('/totalCases', function(result) {
    var totalCases = parseInt(result);
    $('#total-cases').text(totalCases);
});

getResultFromEndpoint('/totalDeaths', function(result) {
    var totalDeaths = parseInt(result);
    $('#total-deaths').text(totalDeaths);
});

getResultFromEndpoint('/totalCasesCountry', function(result) {
    var totalCasesGr = result['Greece'];
    $('#total-cases-gr').text(totalCasesGr);
});

getResultFromEndpoint('/totalDeathsCountry', function(result) {
    var totalDeathsGr = result['Greece'];
    $('#total-deaths-gr').text(totalDeathsGr);
});

getResultFromEndpoint('/totalDays', function(result) {
    $('#time-frame').text('Από: ' + result['first'] + '  Μέχρι: ' + result['last']);
});

getResultFromEndpoint('/casesEU', function(result) {
    $('#cases-EU').text(result);
});

getResultFromEndpoint('/casesnonEU', function(result) {
    $('#cases-Non-EU').text(result);
});

getResultFromEndpoint('/deathsEU', function(result) {
    $('#deaths-EU').text(result);
});

getResultFromEndpoint('/deathsnonEU', function(result) {
    $('#deaths-Non-EU').text(result);
});

getResultFromEndpoint('/cases_todayEU', function(result) {
    $('#casesTodayEU').text(result);
});

getResultFromEndpoint('/cases_today_nonEU', function(result) {
    $('#casesTodayNonEU').text(result);
});

getResultFromEndpoint('/cases_today_global', function(result) {
    $('#casesTodayGlobal').text(result);
});

getResultFromEndpoint('/deaths_today_EU', function(result) {
    $('#deathsTodayEU').text(result);
});

getResultFromEndpoint('/deaths_today_nonEU', function(result) {
    $('#deathsTodayNonEU').text(result);
});

getResultFromEndpoint('/deaths_today_global', function(result) {
    $('#deathsTodayGlobal').text(result);
});

getResultFromEndpoint('/recovered_greece', function(result) {
    $('#recovered_greece').text(result);
});

getResultFromEndpoint('/getCountries', function(result) {
    var select1 = document.getElementById("selectField1");
    var select2 = document.getElementById("selectField2");

    // create option for all countries together
    var el = document.createElement("option");
    el.textContent = 'WORLD';
    el.value = 'WORLD';
    el.setAttribute('selected','selected');
    var el2 = el.cloneNode(true);
    select1.appendChild(el);
    select2.appendChild(el2);

    // for the second graph of death ratios
    var select3 = document.getElementById("selectFieldDeath1");
    var select4 = document.getElementById("selectFieldDeath2");
    var el3 = el.cloneNode(true);
    var el4 = el.cloneNode(true);
    select3.appendChild(el3);
    select4.appendChild(el4);

    // append other options from country list
    for (var i = 0; i < result.length; i++) {
        var opt = result[i];
        el = document.createElement("option");
        el.textContent = opt;
        el.value = opt;
        el2 = el.cloneNode(true);
        select1.appendChild(el);
        select2.appendChild(el2);

        // for the second graph of death ratios
        el3 = el.cloneNode(true);
        el4 = el.cloneNode(true);
        select3.appendChild(el3);
        select4.appendChild(el4);
    }
});

$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: path,
        dataType: "text",
        success: function(data) {processRawData(data);}
     });
});



