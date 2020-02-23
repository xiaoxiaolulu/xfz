function Banner() {
    this.bannerWidth = 798;
    this.bannerGroup = $("#banner-group");
    this.index = 1;
    this.leftArrow = $('.left-arrow');
    this.rightArrow = $('.right-arrow');
    this.bannerUrl = $('#banner-url');
    this.liList = this.bannerUrl.children("li");
    this.bannerCount = this.liList.length;
}

Banner.prototype.initBanner = function () {
    var self = this;
    var firstBanner = self.liList.eq(0).clone();
    var lastBanner = self.liList.eq(self.bannerCount - 1).clone();
    self.bannerUrl.append(firstBanner);
    self.bannerUrl.prepend(lastBanner);
    this.bannerUrl.css({"width": self.bannerWidth * (self.bannerCount + 2), "left": -self.bannerWidth});
};

Banner.prototype.initPageControl = function () {
    var self = this;
    var pageControl = $(".page-control");
    for (let i = 0; i < self.bannerCount; i++) {
        var circle = $("<li></li>");
        pageControl.append(circle);
        if (i === 0) {
            circle.addClass("active");
        }
    }
    pageControl.css({"width": 10 * self.bannerCount + 8 * 2 + 16 * (self.bannerCount - 1)})
};

Banner.prototype.toggleArrow = function (isShow) {
    var self = this;
    if (isShow) {
        self.leftArrow.show();
        self.rightArrow.show();
    } else {
        self.leftArrow.hide();
        self.rightArrow.hide();
    }
};

Banner.prototype.listenBannerHover = function () {
    var self = this;
    this.bannerGroup.hover(function () {
        clearInterval(self.timer);
        self.toggleArrow(true);
    }, function () {
        self.loop();
        self.toggleArrow(false);
    });
};

Banner.prototype.loop = function () {
    var self = this;
    var bannerUrl = document.getElementById('banner-url');
    this.timer = setInterval(function () {
        if (self.index >= self.bannerCount + 1) {
            self.bannerUrl.css({"left": -self.bannerWidth});
            self.index = 2;
            bannerUrl.style.left = self.index + 'px';
        } else {
            self.index++;
            bannerUrl.style.left = bannerUrl.offsetLeft + -798 * self.index + 'px';
        }
    }, 1000);
};

Banner.prototype.listenArrowClick = function () {
    var self = this;
    var bannerUrl = document.getElementById('banner-url');
    self.leftArrow.click(function () {
        if (self.index === 0) {
            self.bannerUrl.css({"left": -self.bannerCount * self.bannerWidth});
            self.index = self.bannerCount - 1;
        } else {
            self.index--;
        }
        bannerUrl.style.left = bannerUrl.offsetLeft + -798 * self.index + 'px';
    });

    self.rightArrow.click(function () {
        if (self.index === self.bannerCount + 1) {
            self.bannerUrl.css({"left": -self.bannerWidth});
            self.index = 2;
        } else {
            self.index++;
        }
        bannerUrl.style.left = bannerUrl.offsetLeft + -798 * self.index + 'px';
    })
};

Banner.prototype.listenBannerControl = function () {
    var self = this;
    var pageControl = $(".page-control");
    pageControl.children('li').each(function (index, obj) {
        $(obj).click(function () {
            self.index = index;
            var bannerUrl = document.getElementById('banner-url');
            bannerUrl.style.left = bannerUrl.offsetLeft + -798 * self.index + 'px';

            if (index === 0) {
                index = self.bannerCount - 1;
            } else if (index === self.bannerCount + 1) {
                index = 0
            } else {
                index = self.index - 1
            }
            pageControl.children('li').eq(index).addClass('active').siblings().removeClass('active');
        })
    })
};

Banner.prototype.run = function () {
    this.initBanner();
    this.initPageControl();
    this.loop();
    this.listenBannerHover();
    this.listenArrowClick();
    this.listenBannerControl();
};

function Index() {
    var self = this;
    self.page = 2;
    self.category_id = 0;

    template.defaults.imports.timeSince = function (dataValue) {
        var date = new Date(dataValue);
        var dates = date.getTime();
        var nows = (new Date()).getTime();
        var timestamp = (nows - dates) / 1000;
        if (timestamp < 60) {
            return '刚刚';
        } else if (timestamp >= 60 && timestamp < 60 * 60) {
            var minutes = parseInt(timestamp / 60);
            return minutes + '分钟前';
        } else if (timestamp >= 60 * 60 && timestamp < 60 * 60 * 24) {
            var hours = parseInt(timestamp / 60 / 60);
            return hours + '小时前';
        } else if (timestamp >= 60 * 60 * 24 && timestamp < 60 * 60 * 24 * 30) {
            var days = parseInt(timestamp / 60 / 60 / 24);
            return days + '天前';
        } else {
            var year = date.getFullYear();
            var month = date.getMonth();
            var day = date.getDate();
            var hour = date.getHours();
            var minute = date.getMinutes();
            return year + '/' + month + '/' + day + ' ' + hour + ':' + minute;
        }
    };
}

Index.prototype.listenLoadMoreEvent = function () {
    var self = this;
    var loadBtn = $("#load-more-btn");
    loadBtn.click(function () {
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'categroy_id': self.category_id,
                'p': self.page
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    // console.log(result['data']);
                    var newses = result['data'];
                    if (newses.length > 0) {
                        var tpl = template("news-item", {"newses": newses});
                        var ul = $(".list-inner-group");
                        ul.append(tpl);
                        self.page += 1;
                    } else {
                        loadBtn.hide();
                    }
                }
            }
        });
    });
};

Index.prototype.listenCategorySwitchEvent = function () {
    var tabGroup = $(".list-tab");
    tabGroup.children().click(function () {
        var li = $(this);
        var category_id = li.attr('data-category');
        var page = 1;
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'category_id': category_id,
                'p': page
            },
            'success': function (result) {
                if(result['code']===200){
                    var newses = result['data'];
                    var tp1 = template("news-item", {'newses': newses});
                    var newsListGroup = $(".list-inner-group");
                    newsListGroup.empty();
                    newsListGroup.append(tp1);
                    self.page = 2;
                    self.category_id = category_id;
                    li.addClass("active").siblings().removeClass('active');
                    var loadBtn = $("#load-more-btn");
                    loadBtn.show();
                }
            }
        });
    });
};

Index.prototype.run = function () {
    var self = this;
    self.listenLoadMoreEvent();
    self.listenCategorySwitchEvent();
};

$(function () {
    var banner = new Banner();
    banner.run();

    var index = new Index();
    index.run();
});
