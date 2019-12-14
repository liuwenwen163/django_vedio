$('#comment-submit').click(function () {
    var content = $('#comment-content').val();
    var csrfToken = $('#django-csrf-token').val();
    var videoId = $(this).attr('data-video-id');
    var userId = $(this).attr('data-user-id');
    var url = $(this).attr('data-url');
    var ajax_comment_show = $('#ajax-comment-show')

    if(!content) {
        alert('评论不能为空');
        return;
    };

    $.ajax({
       url: url,
       data: {
           content: content,
           videoId: videoId,
           userId: userId,
           csrfmiddlewaretoken: csrfToken
       },
        type: 'post',
        success: function(data){
           if (data.code==0){
               window.location.href = '/client/video/' + videoId
           }else {
                alert(data.msg)
            }

        },
        fail: function (e) {
            console.log('error:%s', e)
        }
    });

    // console.log(videoId, userId);
});
