/*
**************************Navbar**************************
*/

// Changes the value of the number of contestants slider in Filter
function numberSlider() {
    document.getElementById('numberOfContestantsValue').innerText = document.getElementById('numberOfContestants').value;
}

// Selects all categories when the select all checkbox is checked
$(document).ready(function () {
    $('#selectAllCategories').change(function () {
        $('input[name="kategory"]').prop('checked', $(this).prop('checked'));
    });
});

/*
***********************************************************
*/
