
function News() {
    
};

News.prototype.run = function () {
    var self = this;
    // self.listenOploadFileEvent();
    self.initUEditor();
    self.listenSubmitEvent();
    self.listenQiniuUploadFileEvent();
};

//监听提交按钮
News.prototype.listenSubmitEvent = function(){
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-news-id')
        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();
        if(pk){
            url = '/cms/edit_news/'
        }else{
            url = '/cms/write_news/'
        }
        xfzajax.post({
            'url': url,
            'data':{
                'title':title,
                'category':category,
                'desc':desc,
                'thumbnail':thumbnail,
                'content':content,
                'pk':pk,
            },
            'success':function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('新闻发表成功！',function () {
                        window.location.reload();
                    })
                }
            }
        })
    })
}

//初始化编辑器
News.prototype.initUEditor = function(){
    window.ue = UE.getEditor('editor',{
        'initialFrameHeight':400,
        'serverUrl':'/ueditor/upload/',
    })
}

//监听文件上传按钮
News.prototype.listenOploadFileEvent = function(){
    var upLoadBtn = $('#thumbnail-btn');
    upLoadBtn.change(function () {
        var file = upLoadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file',file);
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data':formData,
            'processData':false,
            'contentType':false,
            'success':function (result) {
                if(result['code'] === 200){
                    var url = result['data']['url'];
                    var thumbnailInput = $('#thumbnail-form');
                    thumbnailInput.val(url);
                }
            }
        })

    })
}

//七牛云上传进度函数
News.prototype.handleFileUploadProgress = function(response){
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed(0)+"%"
    var progressGroup = $('#progress-group');
    progressGroup.show();
    var progressBar = $(".progress-bar");
    progressBar.css({'width':percentText})
    progressBar.text(percentText)

}
//七牛云上传错误函数
News.prototype.handleFileUploadError = function(error){
    window.messageBox.showError(error,message);
    var progressGroup = $('#progress-group')
    progressGroup.hide();
}
//七牛云上传成功函数
News.prototype.handleFileUploadComplete = function(response){
    var progressGroup = $('#progress-group')
    progressGroup.hide();

    var domain = 'http://py8j0b6fg.bkt.clouddn.com/';
    var filename = response.key;
    var url = domain+filename;
    var thumbnailInput = $("input[name='thumbnail']");
    thumbnailInput.val(url);
}

//文件上传到七牛云
News.prototype.listenQiniuUploadFileEvent = function(){
    var self = this;
    var upLoadBtn = $('#thumbnail-btn');
    upLoadBtn.change(function () {
        var file = this.files[0]
        xfzajax.get({
            'url':'/cms/qntoken/',
            'success':function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token']
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                    var putExtra = {
                        filename:key,
                        params:{},
                        mimeType:['image/png','image/jpeg','image/gif']
                    }
                    var config = {
                        useCdnDomain:true,
                        retryCount:6,
                        region: qiniu.region.z2
                    };
                    var objservable = qiniu.upload(file,key,token,putExtra,config);
                    objservable.subscribe({
                        'next':self.handleFileUploadProgress,
                        'error':self.handleFileUploadError,
                        'complete':self.handleFileUploadComplete,
                    });
                }
            }
        })
    })
}




$(function () {
    var news = new News();
    news.run()
})