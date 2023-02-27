$( document ).ready(function() {
    $('form#row_number').submit(function(e) {
        e.preventDefault()
        let d = new Date();

        let month = d.getMonth()+1;
        let day = d.getDate();

        let output = d.getFullYear() + '-' +
            (month<10 ? '0' : '') + month + '-' +
            (day<10 ? '0' : '') + day;

        let new_created_field = $('<div>', {class: 'status processing', text: 'Processing'})
        let table_row = jQuery(`<tr> <th scope="row">${output}</th> <td id="status"></td> <td><a href="/">Download</a></td> </tr>`)
        $('#created_files').append(table_row)
        $('#status').append($(new_created_field))
        $(new_created_field).parent().removeAttr('id')

        $.ajax({
            method: 'POST',
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: () => {
                console.log('SUCCESS')
                new_created_field.removeClass('processing')
                new_created_field.addClass('ready')
                new_created_field.text('Ready')
            },
            error: () => {
                console.log('ERROR')
                '<div style="display: none" class="status processing">Processing</div>'
            }
        })
    })
});