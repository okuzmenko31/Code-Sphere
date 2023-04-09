function SignUpForm() {
    const formID = 'form.submit_email_signup'

    $(formID).on('submit', (e) => {
        e.preventDefault();
        var form = $(formID);
        var url = form.attr('action');
        var method = form.attr('method');
        var data = form.serialize();

        $.ajax({
            url: url,
            method: 'POST',
            dataType: 'json',
            data: data,
            success: function (response) {
                var success_message = response.message
                $('.success-message').text(success_message)
                $(formID + ' input').each((index, el) => {
                    $(el).css('border', '1px solid #ced4da');
                });
                $('form.submit_email_signup .invalid-feedback').each((index, el) => {
                    $(el).text('')
                })
            },
            error: function (response) {
                var errors = $.parseJSON(response.responseText);
                var keys = Object.keys(errors.errors)
                var values = Object.values(errors.errors)
                $('form.submit_email_signup .success-message').each((index, el) => {
                    $(el).remove()
                })
                $.each(errors.errors, function (key, value) {
                    var field = document.getElementById('id_' + key)
                    var error_value = value[0]
                    field.style.border = "1px solid red"
                    $(field).siblings('.invalid-feedback').text(error_value);
                });

            }
        });


    });

    $(formID + ' input').focus(function () {
        $(formID).removeClass('is-invalid');
        $(formID).siblings('.invalid-feedback').text('');
        $('.success-message').text('');
        $(formID + ' input').each((index, el) => {
            $(el).css('border', '1px solid #ced4da');
        });
        $(formID + ' input').each((index, el) => {
            $(el).css('border', '1px solid #ced4da');
        });
    });
}

function SignInForm() {
    const formID = 'form.sign_in_form'

    $(formID).on('submit', (e) => {
        e.preventDefault();
        var form = $(formID);
        var url = form.attr('action');
        var method = form.attr('method');
        var data = form.serialize();

        $.ajax({
            url: url,
            method: 'POST',
            dataType: 'json',
            data: data,
            success: function (response) {
                window.location.href = '/codesphere/welcome/'
            },
            error: function (response) {
                var errors = $.parseJSON(response.responseText);
                $.each(errors.errors, function (key, value) {
                    $('.form-errors').text(value[0])
                });

            }
        });


    });

    $(formID + ' input').focus(function () {
        $(formID).removeClass('is-invalid');
        $(formID).siblings('.invalid-feedback').text('');
    });
}

$(document).ready(() => {
    SignUpForm();
    SignInForm();
});