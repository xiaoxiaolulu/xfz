function Banner() {
    this.bannerWidth = 798;
    this.bannerGroup = $("#banner-group");
    this.listenBannerHover();
    this.index = 1;
    this.leftArrow = $(".left-arrow");
    this.rightArrow = $(".right-arrow");
    this.bannerUl = $("#banner-ul");
    this.liList = this.bannerUl.children("li");
    this.bannerCount = this.liList.length;
    this.pagecontrol = $('.page-control');
}

Banner.prototype.initBanner = function () {
    var self = this;
    var firstBanner = self.liList.eq(0).clone()
    var lastBanner = self.liList.eq(self.bannerCount - 1).clone()
    self.bannerUl.append(firstBanner);
    self.bannerUl.prepend(lastBanner);

    self.bannerUl.css({'width': (self.bannerCount + 2) * self.bannerWidth, 'left': -self.bannerWidth})

}

Banner.prototype.initPageControl = function () {
    var self = this;
    for (var i = 0; i < self.bannerCount; i++) {
        var circle = $("<li></li>");
        self.pagecontrol.append(circle);
        if (i === 0) {
            circle.addClass('active');
        }
    }
    self.pagecontrol.css({'width': self.bannerCount * 12 + 8 * 2 + 16 * (self.bannerCount - 1)})

}

Banner.prototype.toggleArrow = function (isShow) {
    var self = this;
    if (isShow) {
        self.leftArrow.show()
        self.rightArrow.show()
    } else {
        self.leftArrow.hide()
        self.rightArrow.hide()
    }
}

Banner.prototype.listenBannerHover = function () {
    var self = this;
    this.bannerGroup.hover(function () {
        clearInterval(self.timer)
        self.toggleArrow(true)
    }, function () {
        self.loop()
        self.toggleArrow(false)
    });
}

Banner.prototype.animate = function () {
    var self = this
    self.bannerUl.stop().animate({'left': -798 * self.index}, 500)
    var index = self.index;
    if (index === 0) {
        index = self.bannerCount - 1;
    } else if (index === self.bannerCount + 1) {
        index = 0;
    } else {
        index = self.index - 1;
    }
    self.pagecontrol.children("li").eq(index).addClass('active').siblings().removeClass('active');

}

Banner.prototype.loop = function () {
    var self = this;
    this.timer = setInterval(function () {
        if (self.index >= self.bannerCount + 1) {
            self.bannerUl.css({'left': -self.bannerWidth})
            self.index = 2;
        } else {
            self.index += 1;
        }
        self.animate();
    }, 2000);
}

Banner.prototype.listenArrowClick = function () {
    var self = this;
    self.leftArrow.click(function () {
        if (self.index === 0) {
            self.bannerUl.css({'left': -self.bannerWidth * self.bannerCount})
            self.index = self.bannerCount - 1;
        } else {
            self.index--;
        }
        self.animate();
    })

    self.rightArrow.click(function () {
        if (self.index === self.bannerCount + 1) {
            self.bannerUl.css({'left': -self.bannerWidth})
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate();
    })
}

Banner.prototype.listenPageControl = function () {
    var self = this;
    self.pagecontrol.children("li").each(function (index, obj) {
        $(obj).click(function () {
            self.index = index;
            self.animate();

        });
    })

}


Banner.prototype.run = function () {
    this.initBanner()
    this.loop()
    this.listenArrowClick()
    this.initPageControl()
    this.listenPageControl()
}

function Index() {
    var self = this
    self.page = 2;
    self.category_id = 0;
    self.loadBtn = $('#load-more-btn');

};

Index.prototype.run = function () {
    var self = this;
    self.listenLoadMoreEvent();
    self.listenCategoryEvent();
}

//监听加载更多按钮
Index.prototype.listenLoadMoreEvent = function () {
    var self = this;
    self.loadBtn.click(function () {
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'p': self.page,
                'category_id': self.category_id
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data'];
                    if (newses.length > 0) {
                        var tpl = template("news-item", {"newses": newses});
                        var ul = $(".list-inner-group");
                        ul.append(tpl);
                        self.page += 1;
                    } else {
                        self.loadBtn.hide()
                    }
                }
            }
        })
    })
}

//监听分类按钮
Index.prototype.listenCategoryEvent = function () {
    var self = this;
    var tabGroup = $('.list-tab');
    tabGroup.children().click(function () {
        //this代表当前选中li标签
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
                if (result['code'] === 200) {
                    var newses = result['data']
                    var tpl = template("news-item", {"newses": newses});
                    //将当前标签下的所有子元素删掉
                    var newsListGroup = $('.list-inner-group')
                    newsListGroup.empty();
                    newsListGroup.append(tpl)
                    self.page = 2;
                    self.category_id = category_id;
                    li.addClass('active').siblings().removeClass('active')
                    self.loadBtn.show()
                }
            }
        })

    })
}


$(function () {
    var banner = new Banner();
    banner.run();
    var index = new Index();
    index.run();

})