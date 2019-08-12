

jQuery(document).ready(function () {
    reasonList = ['Лікарняний', 'Відрядження', 'Курси'];
    var n = -1;

    jQuery('#pnl').load('../repltable/');

});



function reasEnter() {
    n = -1;
}

function genReplhist() {
      console.log(jQuery('#file-input').val());
      data['filename'] = jQuery('#file-input').val()
      jQuery.ajax({
            url: "../repl_3/",
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
    console.log("Додаємо")
    data = {};
    data['datepicker1'] = $('#datepicker1').val();
    data['datepicker1'] = $('#datepicker1').val();
    data['teacher'] = $('#teacher').val();
    data['reason'] = $('#reason').val();

    jQuery.ajax({
            url: "../missgen/",
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
    jQuery('#pnl').load('../repltable/');
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

// function genRepl() {
//     //Обробка кнопки початку генерації таблиці замін
//     console.log("aaaaaaaaaaaaa");
//     //Генеруємо
//     var data = $("#update-form2").serialize();
//     jQuery.ajax({
//         url: "../replgen/",
//         type: "POST",
//         cache: false,
//         data: data,
//         error: function () {
//             console.log("Щось не те");
//         },
//         success: function () {
//             jQuery('#pnl').load('../repltable/');
//             //Зберігаємо поля дат
//
//         }
//     });
// }