var inputNumber = $('#number'); //传递集数的参数
var inputUrl = $('#url');  //传递视频url的参数
//传递videosub_id给hidden的元素，这样就可以根据据参数为空或者有值进行对应的操作了
var videosubInputId = $('#videosub-input-id');


$('.update-btn').click(function(){
    var videosubId = $(this).attr('data-id');
    var videoSubNumber = parseInt($(this).attr('data-number'));
    var videoSubUrl = $(this).attr('data-url');

    inputNumber.val(videoSubNumber);
    inputUrl.val(videoSubUrl);
    videosubInputId.val(videosubId);
});

