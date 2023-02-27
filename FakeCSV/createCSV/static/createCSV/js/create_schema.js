$( document ).ready(function() {
    $('#add_column').submit( function (e) {
        let $fieldset = $('#add_column fieldset')
        let $order = $('#add_column fieldset :input[name="order"]')

        $fieldset.attr('name', $order.attr('name')+'_'+$order.val())
        let clone = $fieldset.clone()
        $('#columns').append(clone)
        clone.find('select[name="column_type"]').val($fieldset.find('select[name="column_type"]').val())
        e.preventDefault()
    })


    $('#columns').submit( function (e) {
        let data = {
            schema_data: {},
            columns: {}
        }

        $('form#schema_info').find('input, select').each((field_id, field) => {
            data.schema_data[field['name']] = field['value']
        })

        $('#columns fieldset').each((fieldset_id, fieldset) => {
            let column = {}
            $(fieldset).find('input, select').each((id, elem)=>{
                column[elem['name']] = elem['value']
            })
            data.columns[fieldset_id] = column
        })

        console.log(data)
        e.preventDefault()

        $.ajax({
            method: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            type: this.method,
            url: this.action,
            data: data,
            dataType: 'json',
            success: (response) => {
                let info = $('#info')
                info.addClass('alert-success')
                info.empty()
                $('<span>Success: Your schema completed, more info on schemas</span>').appendTo(info);
            },
            error: (error) => {
                let info = $('#info')
                info.empty()
                info.addClass('alert-danger')
                $(`<span>${error}</span>`).appendTo(info);
            }
        })
    })

});