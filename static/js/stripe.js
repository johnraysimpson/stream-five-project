$(function(){
    $('#payment-form').submit(function() {
        var form = this;
        var card = {
            number: $('#id_credit_card_number').val(), //name in the MakePaymentsForm preceeded by 'id_'
            expMonth: $('#id_expiry_month').val(), //name in the MakePaymentsForm preceeded by 'id_'
            expYear: $('#id_expiry_year').val(), //name in the MakePaymentsForm preceeded by 'id_'
            cvc: $('#id_cvv').val() //name in the MakePaymentsForm preceeded by 'id_'
        };
        
    Stripe.createToken(card, function(status, response) {
        if (status === 200) {
            $('#credit-card-errors').hide(); // refers to code in checkout.html
            $('#id_stripe_id').val(response.id); //name in the MakePaymentsForm preceeded by 'id_'
            
            //Prevent the Credit card Detials from being submitted to our server
            $('#id_credit_card_number').removeAttr('name');
            $('#id_cvv').removeAttr('name');
            $('#id_expiry_month').removeAttr('name');
            $('#id_expiry_year').removeAttr('name');
            
            form.submit();
        } else {
            $('#stripe-error-message').text(response.error.message);
            $('#credit-card-errors').show();
            $('#validate_card_btn').attr('disabled', false);
        }
    });
    return false;
    });
});