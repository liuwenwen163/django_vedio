$('#regist-submit').click(function () {
    var username = $('#username').val();
    var password = $('#password').val();
    var url = $(this).attr('data-url');
    var csrfToken = $('#django-csrf-token').val();

    if (!username || !password){
        alert('缺少必要字段');
        return;
    }

    //使用ajax之后，登录后的提示信息不需要刷新，直接就可以返回给前端了
    $.ajax({
        url: url,
        type: 'post',
        data: {
            username: username,
            password: password,
            csrfmiddlewaretoken: csrfToken
        },
        success: function (data) {
            alert(data.msg)
        },
        fail: function(e){
            console.log('error:%s', e)
        }
    });
});

$('#login-submit').click(function () {
    var username = $('#username').val();
    var password = $('#password').val();
    var url = $(this).attr('data-url');
    var csrfToken = $('#django-csrf-token').val();

    if (!username || !password){
        alert('缺少必要字段');
        return;
    }

    //使用ajax之后，登录后的提示信息不需要刷新，直接就可以返回给前端了
    $.ajax({
        url: url,
        type: 'post',
        data: {
            username: username,
            password: password,
            csrfmiddlewaretoken: csrfToken
        },
        success: function (data) {
            if (data.code) {
                alert(data.msg)
            }else {
                window.location.href = '/client/video/ex'
            }
        },
        fail: function(e){
            console.log('error:%s', e)
        }
    });
});
