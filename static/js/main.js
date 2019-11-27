$(document).ready(function() {
            
    var vHeight = $(window).height() - (34 + $('.footer').height());
    content_background = $('.content');
    content_background.css({"min-height":vHeight});
        
    $(".alert").children().children().prepend(`<i class="fa fa-exclamation-circle fa-lg" aria-hidden="true"></i>`)  
    
    var days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
    
    for(let i=0; i < days.length; i++) {
        $(`#day-wrapper-${days[i]}`).hide();
        
        $(`#hide-day-button-${days[i]}`).hide();
        
        $(`#show-day-button-${days[i]}`).click(function() {
            $(`#day-wrapper-${days[i]}`).slideDown('slow');
            $(`#show-day-button-${days[i]}`).hide();
            $(`#hide-day-button-${days[i]}`).show();
        });
        
        $(`#hide-day-button-${days[i]}`).click(function() {
            $(`#day-wrapper-${days[i]}`).slideUp('slow');
            $(`#show-day-button-${days[i]}`).show();
            $(`#hide-day-button-${days[i]}`).hide();
        });
    }
    
    $(`#unpaid-wrapper`).hide();
    
    $(`#hide-unpaid-button`).hide();
    
    $(`#show-unpaid-button`).click(function() {
            $(`#unpaid-wrapper`).slideDown('slow');
            $(`#show-unpaid-button`).hide();
            $(`#hide-unpaid-button`).show();
    });
    
    $(`#hide-unpaid-button`).click(function() {
            $(`#unpaid-wrapper`).slideUp('slow');
            $(`#show-unpaid-button`).show();
            $(`#hide-unpaid-button`).hide();
    });
    
    $('.masterTooltip').hover(function(){
        // Hover over code
        var title = $(this).attr('title');
        $(this).data('tipText', title).removeAttr('title');
        $('<p class="newtooltip"></p>')
        .append(title)
        .appendTo($('.container'))
        .fadeIn('slow');
    }, function() {
        // Hover out code
        $(this).attr('title', $(this).data('tipText'));
        $('.newtooltip').remove();
    })
    .mousemove(function(e) {
        var mousex = e.pageX + 20; //Get X coordinates
        var mousey = e.pageY + 10; //Get Y coordinates
        $('.newtooltip')
        .css({
            top: mousey, 
            left: mousex
            });
    });
});
    