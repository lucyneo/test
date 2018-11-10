




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


        $('#username2').editable({
            type: "text2",                //编辑框的类型。支持text|textarea|select|date|checklist等
            title: "用户名2",              //编辑框的标题
            disabled: false,             //是否禁用编辑
            emptytext: "空文本",          //空值的默认文本
            mode: "inline",              //编辑框的模式：支持popup和inline两种模式，默认是popup
            validate: function (value) { //字段验证
                if (!$.trim(value)) {
                    return '不能为空';
                }
            }
        });


});

