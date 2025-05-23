"use strict";
function _typeof(t) {
  return (_typeof =
    "function" == typeof Symbol && "symbol" == typeof Symbol.iterator
      ? function (t) {
          return typeof t;
        }
      : function (t) {
          return t &&
            "function" == typeof Symbol &&
            t.constructor === Symbol &&
            t !== Symbol.prototype
            ? "symbol"
            : typeof t;
        })(t);
}
jQuery(document).ready(function (i) {
  var s = {},
    o = !1;
  (s.showOverlay = function () {
    i("body").addClass("show-main-overlay");
  }),
    (s.hideOverlay = function () {
      i("body").removeClass("show-main-overlay");
    }),
    (s.showMessage = function () {
      i("body").addClass("show-message"), (o = !0);
    }),
    (s.hideMessage = function () {
      i("body").removeClass("show-message"),
        i("#main .message-list li").removeClass("active"),
        (o = !1);
    }),
    (s.showSidebar = function () {
      i("body").addClass("show-sidebar");
    }),
    (s.hideSidebar = function () {
      i("body").removeClass("show-sidebar");
    }),
    i(".trigger-toggle-sidebar").on("click", function () {
      s.showSidebar(), s.showOverlay();
    }),
    i(".trigger-message-close").on("click", function () {
      s.hideMessage(), s.hideOverlay();
    }),
    i("#main .message-list li").on("click", function (t) {
      var e = i(this);
      i(t.target).is("label")
        ? e.toggleClass("selected")
        : o && e.is(".active")
        ? (s.hideMessage(), s.hideOverlay())
        : (o
            ? (s.hideMessage(),
              e.addClass("active"),
              setTimeout(function () {
                s.showMessage();
              }, 300))
            : (e.addClass("active"), s.showMessage()),
          s.showOverlay());
    }),
    i("#main > .overlay").on("click", function () {
      s.hideOverlay(), s.hideMessage(), s.hideSidebar();
    });
});
var quill = new Quill("#snow-editor", {
  theme: "snow",
  modules: {
    toolbar: [
      [{ font: [] }, { size: [] }],
      ["bold", "italic", "underline"],
      [{ color: [] }, { background: [] }],
      [{ list: "ordered" }, { list: "bullet" }],
    ],
  },
});
!(function (s, o, i) {
  var r, h, n, a, c, e, p, d, l, g, u, v, f, S, t, m, y, b, w, T, $, x, C;
  function H(t, e) {
    (this.el = t),
      (this.options = e),
      (h = h || y()),
      (this.$el = s(this.el)),
      (this.doc = s(this.options.documentContext || i)),
      (this.win = s(this.options.windowContext || o)),
      (this.$content = this.$el.children("." + e.contentClass)),
      this.$content.attr("tabindex", this.options.tabIndex || 0),
      (this.content = this.$content[0]),
      this.options.iOSNativeScrolling &&
      null != this.el.style.WebkitOverflowScrolling
        ? this.nativeScrolling()
        : this.generate(),
      this.createEvents(),
      this.addEvents(),
      this.reset();
  }
  (m = {
    paneClass: "nano-pane",
    sliderClass: "nano-slider",
    contentClass: "nano-content",
    iOSNativeScrolling: !1,
    preventPageScrolling: !1,
    disableResize: !1,
    alwaysVisible: !1,
    flashDelay: 1500,
    sliderMinHeight: 20,
    sliderMaxHeight: null,
    documentContext: null,
    windowContext: null,
  }),
    (v = "scroll"),
    (e = "mousedown"),
    (p = "mousemove"),
    (l = "mousewheel"),
    (d = "mouseup"),
    (u = "resize"),
    (c = "drag"),
    (S = "up"),
    (n = "DOMMouseScroll"),
    (a = "down"),
    (f = "touchmove"),
    (r =
      "Microsoft Internet Explorer" === o.navigator.appName &&
      /msie 7./i.test(o.navigator.appVersion) &&
      o.ActiveXObject),
    (h = null),
    (T = o.requestAnimationFrame),
    (t = o.cancelAnimationFrame),
    (x = i.createElement("div").style),
    (C = (function () {
      for (
        var t,
          e = ["t", "webkitT", "MozT", "msT", "OT"],
          i = (t = 0),
          s = e.length;
        t < s;
        i = ++t
      )
        if ((e[i], e[i] + "ransform" in x))
          return e[i].substr(0, e[i].length - 1);
      return !1;
    })()),
    ($ = (function (t) {
      return (
        !1 !== C && ("" === C ? t : C + t.charAt(0).toUpperCase() + t.substr(1))
      );
    })("transform")),
    (b = !1 !== $),
    (y = function () {
      var t = i.createElement("div"),
        e = t.style;
      return (
        (e.position = "absolute"),
        (e.width = "100px"),
        (e.height = "100px"),
        (e.overflow = v),
        (e.top = "-9999px"),
        i.body.appendChild(t),
        (e = t.offsetWidth - t.clientWidth),
        i.body.removeChild(t),
        e
      );
    }),
    (w = function () {
      var t = o.navigator.userAgent,
        e = /(?=.+Mac OS X)(?=.+Firefox)/.test(t);
      return (
        !!e &&
        ((t = (t = /Firefox\/\d{2}\./.exec(t)) && t[0].replace(/\D+/g, "")),
        e && 23 < +t)
      );
    }),
    (H.prototype.preventScrolling = function (t, e) {
      this.isActive &&
        (t.type === n
          ? ((e === a && 0 < t.originalEvent.detail) ||
              (e === S && t.originalEvent.detail < 0)) &&
            t.preventDefault()
          : t.type === l &&
            t.originalEvent &&
            t.originalEvent.wheelDelta &&
            ((e === a && t.originalEvent.wheelDelta < 0) ||
              (e === S && 0 < t.originalEvent.wheelDelta)) &&
            t.preventDefault());
    }),
    (H.prototype.nativeScrolling = function () {
      this.$content.css({ WebkitOverflowScrolling: "touch" }),
        (this.iOSNativeScrolling = !0),
        (this.isActive = !0);
    }),
    (H.prototype.updateScrollValues = function () {
      var t = this.content;
      (this.maxScrollTop = t.scrollHeight - t.clientHeight),
        (this.prevScrollTop = this.contentScrollTop || 0),
        (this.contentScrollTop = t.scrollTop),
        this.iOSNativeScrolling ||
          ((this.maxSliderTop = this.paneHeight - this.sliderHeight),
          (this.sliderTop =
            0 === this.maxScrollTop
              ? 0
              : (this.contentScrollTop * this.maxSliderTop) /
                this.maxScrollTop));
    }),
    (H.prototype.setOnScrollStyles = function () {
      var t, e;
      b
        ? ((t = {})[$] = "translate(0, " + this.sliderTop + "px)")
        : (t = { top: this.sliderTop }),
        T
          ? this.scrollRAF ||
            (this.scrollRAF = T(
              ((e = this),
              function () {
                (e.scrollRAF = null), e.slider.css(t);
              })
            ))
          : this.slider.css(t);
    }),
    (H.prototype.createEvents = function () {
      var e, i, s, o, n, l, r;
      this.events = {
        down: function (t) {
          return (
            (r.isBeingDragged = !0),
            (r.offsetY = t.pageY - r.slider.offset().top),
            r.pane.addClass("active"),
            r.doc.bind(p, r.events[c]).bind(d, r.events.up),
            !1
          );
        },
        drag: function (t) {
          return (
            (l.sliderY = t.pageY - l.$el.offset().top - l.offsetY),
            l.scroll(),
            l.contentScrollTop >= l.maxScrollTop &&
            l.prevScrollTop !== l.maxScrollTop
              ? l.$el.trigger("scrollend")
              : 0 === l.contentScrollTop &&
                0 !== l.prevScrollTop &&
                l.$el.trigger("scrolltop"),
            !1
          );
        },
        up: function (t) {
          return (
            (n.isBeingDragged = !1),
            n.pane.removeClass("active"),
            n.doc.unbind(p, n.events[c]).unbind(d, n.events.up),
            !1
          );
        },
        resize: function (t) {
          o.reset();
        },
        panedown: function (t) {
          return (
            (s.sliderY =
              (t.offsetY || t.originalEvent.layerY) - 0.5 * s.sliderHeight),
            s.scroll(),
            s.events.down(t),
            !1
          );
        },
        scroll: function (t) {
          i.updateScrollValues(),
            i.isBeingDragged ||
              (i.iOSNativeScrolling ||
                ((i.sliderY = i.sliderTop), i.setOnScrollStyles()),
              null != t &&
                (i.contentScrollTop >= i.maxScrollTop
                  ? (i.options.preventPageScrolling && i.preventScrolling(t, a),
                    i.prevScrollTop !== i.maxScrollTop &&
                      i.$el.trigger("scrollend"))
                  : 0 === i.contentScrollTop &&
                    (i.options.preventPageScrolling && i.preventScrolling(t, S),
                    0 !== i.prevScrollTop && i.$el.trigger("scrolltop"))));
        },
        wheel:
          ((e = i = s = o = n = l = r = this),
          function (t) {
            if (null != t)
              return (
                (t =
                  t.delta ||
                  t.wheelDelta ||
                  (t.originalEvent && t.originalEvent.wheelDelta) ||
                  -t.detail ||
                  (t.originalEvent && -t.originalEvent.detail)) &&
                  (e.sliderY += -t / 3),
                e.scroll(),
                !1
              );
          }),
      };
    }),
    (H.prototype.addEvents = function () {
      var t;
      this.removeEvents(),
        (t = this.events),
        this.options.disableResize || this.win.bind(u, t[u]),
        this.iOSNativeScrolling ||
          (this.slider.bind(e, t[a]),
          this.pane.bind(e, t.panedown).bind(l + " " + n, t.wheel)),
        this.$content.bind(v + " " + l + " " + n + " " + f, t[v]);
    }),
    (H.prototype.removeEvents = function () {
      var t = this.events;
      this.win.unbind(u, t[u]),
        this.iOSNativeScrolling || (this.slider.unbind(), this.pane.unbind()),
        this.$content.unbind(v + " " + l + " " + n + " " + f, t[v]);
    }),
    (H.prototype.generate = function () {
      var t,
        e = this.options,
        i = e.paneClass,
        s = e.sliderClass;
      e.contentClass;
      return (
        this.$el.find("." + i).length ||
          this.$el.find("." + s).length ||
          this.$el.append(
            '<div class="' + i + '"><div class="' + s + '" /></div>'
          ),
        (this.pane = this.$el.children("." + i)),
        (this.slider = this.pane.find("." + s)),
        0 === h && w()
          ? (t = {
              right: -14,
              paddingRight:
                +o
                  .getComputedStyle(this.content, null)
                  .getPropertyValue("padding-right")
                  .replace(/\D+/g, "") + 14,
            })
          : h && ((t = { right: -h }), this.$el.addClass("has-scrollbar")),
        null != t && this.$content.css(t),
        this
      );
    }),
    (H.prototype.restore = function () {
      (this.stopped = !1),
        this.iOSNativeScrolling || this.pane.show(),
        this.addEvents();
    }),
    (H.prototype.reset = function () {
      var t, e, i, s, o, n, l;
      if (!this.iOSNativeScrolling)
        return (
          this.$el.find("." + this.options.paneClass).length ||
            this.generate().stop(),
          this.stopped && this.restore(),
          (n = (i = (t = this.content).style).overflowY),
          r && this.$content.css({ height: this.$content.height() }),
          (e = t.scrollHeight + h),
          0 < (l = parseInt(this.$el.css("max-height"), 10)) &&
            (this.$el.height(""),
            this.$el.height(t.scrollHeight > l ? l : t.scrollHeight)),
          (o =
            (s = this.pane.outerHeight(!1)) +
            parseInt(this.pane.css("top"), 10) +
            parseInt(this.pane.css("bottom"), 10)),
          (l = Math.round((o / e) * o)) < this.options.sliderMinHeight
            ? (l = this.options.sliderMinHeight)
            : null != this.options.sliderMaxHeight &&
              l > this.options.sliderMaxHeight &&
              (l = this.options.sliderMaxHeight),
          n === v && i.overflowX !== v && (l += h),
          (this.maxSliderTop = o - l),
          (this.contentHeight = e),
          (this.paneHeight = s),
          (this.paneOuterHeight = o),
          (this.sliderHeight = l),
          this.slider.height(l),
          this.events.scroll(),
          this.pane.show(),
          (this.isActive = !0),
          t.scrollHeight === t.clientHeight ||
          (this.pane.outerHeight(!0) >= t.scrollHeight && n !== v)
            ? (this.pane.hide(), (this.isActive = !1))
            : this.el.clientHeight === t.scrollHeight && n === v
            ? this.slider.hide()
            : this.slider.show(),
          this.pane.css({
            opacity: this.options.alwaysVisible ? 1 : "",
            visibility: this.options.alwaysVisible ? "visible" : "",
          }),
          ("static" !== (n = this.$content.css("position")) &&
            "relative" !== n) ||
            ((n = parseInt(this.$content.css("right"), 10)) &&
              this.$content.css({ right: "", marginRight: n })),
          this
        );
      this.contentHeight = this.content.scrollHeight;
    }),
    (H.prototype.scroll = function () {
      if (this.isActive)
        return (
          (this.sliderY = Math.max(0, this.sliderY)),
          (this.sliderY = Math.min(this.maxSliderTop, this.sliderY)),
          this.$content.scrollTop(
            (((this.paneHeight - this.contentHeight + h) * this.sliderY) /
              this.maxSliderTop) *
              -1
          ),
          this.iOSNativeScrolling ||
            (this.updateScrollValues(), this.setOnScrollStyles()),
          this
        );
    }),
    (H.prototype.scrollBottom = function (t) {
      if (this.isActive)
        return (
          this.$content
            .scrollTop(this.contentHeight - this.$content.height() - t)
            .trigger(l),
          this.stop().restore(),
          this
        );
    }),
    (H.prototype.scrollTop = function (t) {
      if (this.isActive)
        return (
          this.$content.scrollTop(+t).trigger(l), this.stop().restore(), this
        );
    }),
    (H.prototype.scrollTo = function (t) {
      if (this.isActive)
        return this.scrollTop(this.$el.find(t).get(0).offsetTop), this;
    }),
    (H.prototype.stop = function () {
      return (
        t && this.scrollRAF && (t(this.scrollRAF), (this.scrollRAF = null)),
        (this.stopped = !0),
        this.removeEvents(),
        this.iOSNativeScrolling || this.pane.hide(),
        this
      );
    }),
    (H.prototype.destroy = function () {
      return (
        this.stopped || this.stop(),
        !this.iOSNativeScrolling && this.pane.length && this.pane.remove(),
        r && this.$content.height(""),
        this.$content.removeAttr("tabindex"),
        this.$el.hasClass("has-scrollbar") &&
          (this.$el.removeClass("has-scrollbar"),
          this.$content.css({ right: "" })),
        this
      );
    }),
    (H.prototype.flash = function () {
      var t;
      if (!this.iOSNativeScrolling && this.isActive)
        return (
          this.reset(),
          this.pane.addClass("flashed"),
          setTimeout(function () {
            t.pane.removeClass("flashed");
          }, (t = this).options.flashDelay),
          this
        );
    }),
    (g = H),
    (s.fn.nanoScroller = function (i) {
      return this.each(function () {
        var t, e;
        if (
          ((e = this.nanoscroller) ||
            ((t = s.extend({}, m, i)),
            (this.nanoscroller = e = new g(this, t))),
          i && "object" === _typeof(i))
        ) {
          if ((s.extend(e.options, i), null != i.scrollBottom))
            return e.scrollBottom(i.scrollBottom);
          if (null != i.scrollTop) return e.scrollTop(i.scrollTop);
          if (i.scrollTo) return e.scrollTo(i.scrollTo);
          if ("bottom" === i.scroll) return e.scrollBottom(0);
          if ("top" === i.scroll) return e.scrollTop(0);
          if (i.scroll && i.scroll instanceof s) return e.scrollTo(i.scroll);
          if (i.stop) return e.stop();
          if (i.destroy) return e.destroy();
          if (i.flash) return e.flash();
        }
        return e.reset();
      });
    }),
    (s.fn.nanoScroller.Constructor = g);
})(jQuery, window, document);
