function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    // Hide all content
    tabcontent = document.getElementsByClassName("content");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    
    // Remove "active" class from all buttons
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    // Show the selected content and mark the button as active
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  };

// document.getElementById('slssl').value = "option8";;

$(function() {
    var start = moment().subtract(29, 'days');
    var end = moment();
    function cb(start, end) {
        $('#reportrange span').html(start.format('MMM D, YYYY') + ' - ' + end.format('MMM D, YYYY'));
        $('input[name="calendar_value"]').val(start.format('YYYY-MM-DD') + ':' + end.format('YYYY-MM-DD'));
    }
    // Set the value for the calendar_value input field
    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
        //    'Today': [moment(), moment()],
        //    'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
           'This Quarter': [moment().startOf('quarter'), moment().endOf('quarter')],
           'Last Quarter': [moment().subtract(1, 'quarter').startOf('quarter'), moment().subtract(1, 'quarter').endOf('quarter')]
        }
    }, cb);
    cb(start, end);
});

function downloadTableData() {
    window.location.href = "/downloaddata";
  };

function toggleFormElements() {
    var toggleSwitch = document.getElementById('toggleSwitch');
    var dropdowns = document.querySelectorAll('form select');
    var textbox = document.querySelector('form textarea');
    var submitButton = document.querySelector('form button[type="submit"]');

    if (toggleSwitch.checked) {
        for (var i = 0; i < dropdowns.length; i++) {
            dropdowns[i].disabled = true;
        }
        //reportrange.disabled = true;
        textbox.disabled = false;
        submitButton.disabled = false;
    } else {
        for (var i = 0; i < dropdowns.length; i++) {
            dropdowns[i].disabled = false;
        }
        //reportrange.disabled = false;
        textbox.disabled = true;
        submitButton.disabled = false;
    }
};

function redirecttovalidation() {
    window.location.href = '/validation';
}

document.getElementById("tab1").click();
