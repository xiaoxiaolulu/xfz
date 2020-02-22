function News() {

}

News.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};

News.prototype.run = function () {
    var self = this;
    // self.listenUploadFielEvent();
    self.initUEditor();
    self.listenUploadFielToQiNiuEvent();
    self.listenSubmitEvent();
};

News.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function () {
        event.preventDefault();

        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();

        xfzajax.post({
            'url': '/cms/write_news/',
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    xfzalert.alertSuccess('新闻发表成功！', function () {
                        window.location.reload();
                    })
                }
            }
        })
    })
};

News.prototype.listenUploadFielEvent = function () {
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = result['data']['url'];
                    var thumbnailInput = $('#thumbnail-form');
                    thumbnailInput.val(url);
                    // window.location.reload();
                } else {
                    xfzalert.close();
                    window.messageBox.showError(result['message']);
                }
            }
        })
    });
};

News.prototype.listenUploadFielToQiNiuEvent = function () {
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                    var pubtExtar = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpeg', 'image/gif', 'video/x-ms-wmv']
                    };
                    var config = {
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z0
                    };
                    var objservalbe = qiniu.upload(file, key, token, pubtExtar, config);
                    objservalbe.subscribe({
                        'next': self.handlerFileUploadProgress,
                        'error': self.handlerFileUploadError,
                        'complete': self.handlerFileUploadComplete
                    });
                } else {
                    xfzalert.close();
                    window.messageBox.showError(result['message']);
                }
            }
        })
    });
};

News.prototype.handlerFileUploadProgress = function (response) {
    var total = response.total;
    var percent = total.percent;
    var processGroup = $("#progress-group");
    processGroup.show();
    var processBar = $(".progress-bar");
    processBar.css({"width": percent.toFixed() + '%'});
    processBar.text(percent.toFixed() + "%");
};

News.prototype.handlerFileUploadError = function (error) {
    console.log(error.messsage);
    window.messageBox.showError(error.messsage);
    var processGroup = $("#progress-group");
    processGroup.hide();
};

News.prototype.handlerFileUploadComplete = function (response) {
    console.log(response);
    var processGroup = $("#progress-group");
    processGroup.hide();
    var domain = 'http://q63bbf3xg.bkt.clouddn.com/';
    var filename = response.key;
    var url = domain + filename;
    var thumbnailInput = $("input[name='thumbnail']");
    thumbnailInput.val(url);
};


$(function () {
    var news = new News();
    news.run();
});