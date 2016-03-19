$(function () {
    var $table = $('#table'),
    $remove = $('#remove'),
    selections = [];

    $table.bootstrapTable();
    $(window).resize(function () {
        $table.bootstrapTable('resetView');
    });
});

function detailFormatter(index, row) {
    var html = [];
    $.each(row, function (key, value) {
        html.push('<p><b>' + key + ':</b> ' + value + '</p>');
    });
    return html.join('');
}

function rowStyle(row, index) {
    return {
        classes: row['bootstrap_color']
    };
}

function titleColumnFormatter(value, row, index) {
    return '<a href="' + row['imdb_url'] + '" target="_blank" title="' + row['plot'] + '">' + value + '</a>';
}

function collegeReleaseColumnFormatter(value, row, index) {
    var suffix = '';
    if (!row['college_release_date_confirmed']) {
        suffix = ' <span title="Tentative">(T)</span>';
    }
    return value + suffix;
}

function dateSorter(first, second) {
    if (first && !second) {
        return -1;
    } else if (!first && second) {
        return 1;
    } else if (!first && !second) {
        return 0;
    } else {
        first = moment(first, 'MM-DD-YYYY');
        second = moment(second, 'MM-DD-YYYY');
        return first - second;
    }
}

function grossSorter(first, second) {
    if (first && !second) {
        return 1;
    } else if (!first && second) {
        return -1;
    } else if (!first && !second) {
        return 0;
    } else {
        first = first.replace(/[$€,]/g, '');
        second = second.replace(/[$€,]/g, '');
        return parseInt(first, 10) - parseInt(second, 10);
    }
}
