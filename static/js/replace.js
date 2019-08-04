jQuery(document).ready(function () {
    reasonList = ['Лікарняний', 'Відрядження', 'Курси'];
    var n = -1;
    // tt = jQuery('#worktimeable').val();
    // jQuery('#workttlist').val(tt);

    jQuery('#pnl').load('../repltable/');

});

function reasEnter() {
    n = -1;
}

//TODO виправити некоректність розрахунку початку виділення
function reasType() {

    n++;
    e = jQuery("input[name='reason']");
    text = e.val();
    if (text != '') {
        jQuery.each(reasonList, function (index, value) {
            if (value.indexOf(text) > -1) {
                e.val(value);
                end = value.length;
                setSelectionRange(e[0], n, end);


                // console.log(value);

            }
        });
    }
    ;

}

function add() {
    data = {}
    jQuery.ajax({
            url: "../repladd/",
            type: "POST",
            cache: false,
            data: data,
            error: function () {
                console.log("Щось не те");
            },
            success: function () {
                console.log("Все Ok");
            }
        }
    );

}

function setSelectionRange(input, selectionStart, selectionEnd) {
    if (input.setSelectionRange) {
        input.focus();
        input.setSelectionRange(selectionStart, selectionEnd);
    } else if (input.createTextRange) {
        var range = input.createTextRange();
        range.collapse(true);
        range.moveEnd('character', selectionEnd);
        range.moveStart('character', selectionStart);
        range.select();
    }
}

function setCaretToPos(input, pos) {
    setSelectionRange(input, pos, pos);
}

