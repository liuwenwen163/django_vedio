
var videoEreaStatic = false;
var videoEditArea = $('#video-edit-area')


$('#open-add-video-btn').click(function(){
    //判断下视频区的状态，如果是存在的，就隐藏，不存在就显示
    if (!videoEreaStatic){
        videoEditArea.show();
        videoEreaStatic = true;
    }else{
        videoEditArea.hide();
        videoEreaStatic = false;
    }
})