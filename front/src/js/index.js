function Banner() {
    this.bannerGroup = $("#banner-group");
    this.index = 0;
    this.leftArrow = $('.left-arrow');
    this.rightArrow = $('.right-arrow');
    this.listenBannerHover();
}

Banner.prototype.toggleArrow = function(isShow){
    var self = this;
    if (isShow){
        self.leftArrow.show();
        self.rightArrow.show();
    }else{
        self.leftArrow.hide();
        self.rightArrow.hide();
    }
};


Banner.prototype.listenBannerHover = function(){
    var self = this;
    this.bannerGroup.hover(function(){
        clearInterval(self.timer);
        self.toggleArrow(true);
    },function(){
        self.loop();
        self.toggleArrow(false);
    });
};


Banner.prototype.loop = function(){
    var self = this;
    var bannerUrl = document.getElementById('banner-url');
    this.timer = setInterval(function () {
        if (self.index >= 1){
            self.index = 0;
            bannerUrl.style.left = self.index + 'px';
        } else{
            self.index ++;
            bannerUrl.style.left = bannerUrl.offsetLeft + -798*self.index + 'px';
        }
    }, 1000);
};

Banner.prototype.run = function () {
    this.loop()
};


$(function () {
    var banner = new Banner();
    banner.run();
});
