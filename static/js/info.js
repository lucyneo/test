







$(function () {
        $('#username').editable({
            type: "text",                //编辑框的类型。支持text|textarea|select|date|checklist等
            title: "用户名",              //编辑框的标题
            disabled: false,             //是否禁用编辑
            emptytext: "空文本",          //空值的默认文本
            mode: "inline",              //编辑框的模式：支持popup和inline两种模式，默认是popup
            validate: function (value) { //字段验证
                if (!$.trim(value)) {
                    return '不能为空';
                }
            }
        });

        $('#username').mode()

});





// $('#addButton').on('click', function() {
//             var index = $(this).data('index');
//             if (!index) {
//                 index = 1;
//                 $(this).data('index', 1);
//             }
//             index++;
//             $(this).data('index', index);

//             var template     = $(this).attr('data-template'),
//                 $templateEle = $('#' + template + 'Template'),
//                 $row         = $templateEle.clone().removeAttr('id').insertBefore($templateEle).removeClass('hide'),
//                 $el          = $row.find('input').eq(0).attr('name', template + '[]');
//             $('#defaultForm').bootstrapValidator('addField', $el);

//             // Set random value for checkbox and textbox
//             if ('checkbox' == $el.attr('type') || 'radio' == $el.attr('type')) {
//                 $el.val('Choice #' + index)
//                    .parent().find('span.lbl').html('Choice #' + index);
//             } else {
//                 $el.attr('placeholder', 'Textbox #' + index);
//             }

//             $row.on('click', '.removeButton', function(e) {
//                 $('#defaultForm').bootstrapValidator('removeField', $el);
//                 $row.remove();
//             });
// });