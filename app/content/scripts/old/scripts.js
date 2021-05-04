// Utility function
function Util () {};

/* 
	class manipulation functions
*/
Util.hasClass = function(el, className) {
	if (el.classList) return el.classList.contains(className);
	else return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
};

Util.addClass = function(el, className) {
	var classList = className.split(' ');
 	if (el.classList) el.classList.add(classList[0]);
 	else if (!Util.hasClass(el, classList[0])) el.className += " " + classList[0];
 	if (classList.length > 1) Util.addClass(el, classList.slice(1).join(' '));
};

Util.removeClass = function(el, className) {
	var classList = className.split(' ');
	if (el.classList) el.classList.remove(classList[0]);	
	else if(Util.hasClass(el, classList[0])) {
		var reg = new RegExp('(\\s|^)' + classList[0] + '(\\s|$)');
		el.className=el.className.replace(reg, ' ');
	}
	if (classList.length > 1) Util.removeClass(el, classList.slice(1).join(' '));
};

Util.toggleClass = function(el, className, bool) {
	if(bool) Util.addClass(el, className);
	else Util.removeClass(el, className);
};

Util.setAttributes = function(el, attrs) {
  for(var key in attrs) {
    el.setAttribute(key, attrs[key]);
  }
};

/* 
  DOM manipulation
*/
Util.getChildrenByClassName = function(el, className) {
  var children = el.children,
    childrenByClass = [];
  for (var i = 0; i < el.children.length; i++) {
    if (Util.hasClass(el.children[i], className)) childrenByClass.push(el.children[i]);
  }
  return childrenByClass;
};

Util.is = function(elem, selector) {
  if(selector.nodeType){
    return elem === selector;
  }

  var qa = (typeof(selector) === 'string' ? document.querySelectorAll(selector) : selector),
    length = qa.length,
    returnArr = [];

  while(length--){
    if(qa[length] === elem){
      return true;
    }
  }

  return false;
};

/* 
	Animate height of an element
*/
Util.setHeight = function(start, to, element, duration, cb) {
	var change = to - start,
	    currentTime = null;

  var animateHeight = function(timestamp){  
    if (!currentTime) currentTime = timestamp;         
    var progress = timestamp - currentTime;
    var val = parseInt((progress/duration)*change + start);
    element.style.height = val+"px";
    if(progress < duration) {
        window.requestAnimationFrame(animateHeight);
    } else {
    	cb();
    }
  };
  
  //set the height of the element before starting animation -> fix bug on Safari
  element.style.height = start+"px";
  window.requestAnimationFrame(animateHeight);
};

/* 
	Smooth Scroll
*/

Util.scrollTo = function(final, duration, cb, scrollEl) {
  var element = scrollEl || window;
  var start = element.scrollTop || document.documentElement.scrollTop,
    currentTime = null;

  if(!scrollEl) start = window.scrollY || document.documentElement.scrollTop;
      
  var animateScroll = function(timestamp){
  	if (!currentTime) currentTime = timestamp;        
    var progress = timestamp - currentTime;
    if(progress > duration) progress = duration;
    var val = Math.easeInOutQuad(progress, start, final-start, duration);
    element.scrollTo(0, val);
    if(progress < duration) {
        window.requestAnimationFrame(animateScroll);
    } else {
      cb && cb();
    }
  };

  window.requestAnimationFrame(animateScroll);
};

/* 
  Focus utility classes
*/

//Move focus to an element
Util.moveFocus = function (element) {
  if( !element ) element = document.getElementsByTagName("body")[0];
  element.focus();
  if (document.activeElement !== element) {
    element.setAttribute('tabindex','-1');
    element.focus();
  }
};

/* 
  Misc
*/

Util.getIndexInArray = function(array, el) {
  return Array.prototype.indexOf.call(array, el);
};

Util.cssSupports = function(property, value) {
  if('CSS' in window) {
    return CSS.supports(property, value);
  } else {
    var jsProperty = property.replace(/-([a-z])/g, function (g) { return g[1].toUpperCase();});
    return jsProperty in document.body.style;
  }
};

// merge a set of user options into plugin defaults
// https://gomakethings.com/vanilla-javascript-version-of-jquery-extend/
Util.extend = function() {
  // Variables
  var extended = {};
  var deep = false;
  var i = 0;
  var length = arguments.length;

  // Check if a deep merge
  if ( Object.prototype.toString.call( arguments[0] ) === '[object Boolean]' ) {
    deep = arguments[0];
    i++;
  }

  // Merge the object into the extended object
  var merge = function (obj) {
    for ( var prop in obj ) {
      if ( Object.prototype.hasOwnProperty.call( obj, prop ) ) {
        // If deep merge and property is an object, merge properties
        if ( deep && Object.prototype.toString.call(obj[prop]) === '[object Object]' ) {
          extended[prop] = extend( true, extended[prop], obj[prop] );
        } else {
          extended[prop] = obj[prop];
        }
      }
    }
  };

  // Loop through each object and conduct a merge
  for ( ; i < length; i++ ) {
    var obj = arguments[i];
    merge(obj);
  }

  return extended;
};

// Check if Reduced Motion is enabled
Util.osHasReducedMotion = function() {
  if(!window.matchMedia) return false;
  var matchMediaObj = window.matchMedia('(prefers-reduced-motion: reduce)');
  if(matchMediaObj) return matchMediaObj.matches;
  return false; // return false if not supported
}; 

/* 
	Polyfills
*/
//Closest() method
if (!Element.prototype.matches) {
	Element.prototype.matches = Element.prototype.msMatchesSelector || Element.prototype.webkitMatchesSelector;
}

if (!Element.prototype.closest) {
	Element.prototype.closest = function(s) {
		var el = this;
		if (!document.documentElement.contains(el)) return null;
		do {
			if (el.matches(s)) return el;
			el = el.parentElement || el.parentNode;
		} while (el !== null && el.nodeType === 1); 
		return null;
	};
}

//Custom Event() constructor
if ( typeof window.CustomEvent !== "function" ) {

  function CustomEvent ( event, params ) {
    params = params || { bubbles: false, cancelable: false, detail: undefined };
    var evt = document.createEvent( 'CustomEvent' );
    evt.initCustomEvent( event, params.bubbles, params.cancelable, params.detail );
    return evt;
   }

  CustomEvent.prototype = window.Event.prototype;

  window.CustomEvent = CustomEvent;
}

/* 
	Animation curves
*/
Math.easeInOutQuad = function (t, b, c, d) {
	t /= d/2;
	if (t < 1) return c/2*t*t + b;
	t--;
	return -c/2 * (t*(t-2) - 1) + b;
};


/* JS Utility Classes */
(function() {
  // make focus ring visible only for keyboard navigation (i.e., tab key) 
  var focusTab = document.getElementsByClassName('js-tab-focus');
  function detectClick() {
    if(focusTab.length > 0) {
      resetFocusTabs(false);
      window.addEventListener('keydown', detectTab);
    }
    window.removeEventListener('mousedown', detectClick);
  };

  function detectTab(event) {
    if(event.keyCode !== 9) return;
    resetFocusTabs(true);
    window.removeEventListener('keydown', detectTab);
    window.addEventListener('mousedown', detectClick);
  };

  function resetFocusTabs(bool) {
    var outlineStyle = bool ? '' : 'none';
    for(var i = 0; i < focusTab.length; i++) {
      focusTab[i].style.setProperty('outline', outlineStyle);
    }
  };
  window.addEventListener('mousedown', detectClick);
}());
// File#: _1_accordion
// Usage: codyhouse.co/license
(function() {
  var Accordion = function(element) {
    this.element = element;
    this.items = Util.getChildrenByClassName(this.element, 'js-accordion__item');
    this.showClass = 'accordion__item--is-open';
    this.animateHeight = (this.element.getAttribute('data-animation') == 'on');
    this.multiItems = !(this.element.getAttribute('data-multi-items') == 'off');
    this.initAccordion();
  };

  Accordion.prototype.initAccordion = function() {
    //set initial aria attributes
    for( var i = 0; i < this.items.length; i++) {
      var button = this.items[i].getElementsByTagName('button')[0],
        content = this.items[i].getElementsByClassName('js-accordion__panel')[0],
        isOpen = Util.hasClass(this.items[i], this.showClass) ? 'true' : 'false';
      Util.setAttributes(button, {'aria-expanded': isOpen, 'aria-controls': 'accordion-content-'+i, 'id': 'accordion-header-'+i});
      Util.addClass(button, 'js-accordion__trigger');
      Util.setAttributes(content, {'aria-labelledby': 'accordion-header-'+i, 'id': 'accordion-content-'+i});
    }

    //listen for Accordion events
    this.initAccordionEvents();
  };

  Accordion.prototype.initAccordionEvents = function() {
    var self = this;

    this.element.addEventListener('click', function(event) {
      var trigger = event.target.closest('.js-accordion__trigger');
      //check index to make sure the click didn't happen inside a children accordion
      if( trigger && Util.getIndexInArray(self.items, trigger.parentElement) >= 0) self.triggerAccordion(trigger);
    });
  };

  Accordion.prototype.triggerAccordion = function(trigger) {
    var self = this;
    var bool = (trigger.getAttribute('aria-expanded') === 'true');

    this.animateAccordion(trigger, bool);
  };

  Accordion.prototype.animateAccordion = function(trigger, bool) {
    var self = this;
    var item = trigger.closest('.js-accordion__item'),
      content = item.getElementsByClassName('js-accordion__panel')[0],
      ariaValue = bool ? 'false' : 'true';

    if(!bool) Util.addClass(item, this.showClass);
    trigger.setAttribute('aria-expanded', ariaValue);

    if(this.animateHeight) {
      //store initial and final height - animate accordion content height
      var initHeight = bool ? content.offsetHeight: 0,
        finalHeight = bool ? 0 : content.offsetHeight;
    }

    if(window.requestAnimationFrame && this.animateHeight) {
      Util.setHeight(initHeight, finalHeight, content, 200, function(){
        self.resetContentVisibility(item, content, bool);
      });
    } else {
      self.resetContentVisibility(item, content, bool);
    }

    if( !this.multiItems && !bool) this.closeSiblings(item);

  };

  Accordion.prototype.resetContentVisibility = function(item, content, bool) {
    Util.toggleClass(item, this.showClass, !bool);
    content.removeAttribute("style");
    if(bool && !this.multiItems) { // accordion item has been closed -> check if there's one open to move inside viewport
      this.moveContent();
    }
  };

  Accordion.prototype.closeSiblings = function(item) {
    //if only one accordion can be open -> search if there's another one open
    var index = Util.getIndexInArray(this.items, item);
    for( var i = 0; i < this.items.length; i++) {
      if(Util.hasClass(this.items[i], this.showClass) && i != index) {
        this.animateAccordion(this.items[i].getElementsByClassName('js-accordion__trigger')[0], true);
        return false;
      }
    }
  };

  Accordion.prototype.moveContent = function() { // make sure title of the accordion just opened is inside the viewport
    var openAccordion = this.element.getElementsByClassName(this.showClass);
    if(openAccordion.length == 0) return;
    var boundingRect = openAccordion[0].getBoundingClientRect();
    if(boundingRect.top < 0 || boundingRect.top > window.innerHeight) {
      var windowScrollTop = window.scrollY || document.documentElement.scrollTop;
      window.scrollTo(0, boundingRect.top + windowScrollTop);
    }
  };

  //initialize the Accordion objects
  var accordions = document.getElementsByClassName('js-accordion');
  if( accordions.length > 0 ) {
    for( var i = 0; i < accordions.length; i++) {
      (function(i){new Accordion(accordions[i]);})(i);
    }
  }
}());
// File#: _1_alert
// Usage: codyhouse.co/license
(function() {
    var alertClose = document.getElementsByClassName('js-alert__close-btn');
    if( alertClose.length > 0 ) {
        for( var i = 0; i < alertClose.length; i++) {
            (function(i){initAlertEvent(alertClose[i]);})(i);
        }
    };
}());

function initAlertEvent(element) {
    element.addEventListener('click', function(event){
        event.preventDefault();
        Util.removeClass(element.closest('.js-alert'), 'alert--is-visible');
    });
};
// File#: _1_back-to-top
// Usage: codyhouse.co/license
(function() {
  var backTop = document.getElementsByClassName('js-back-to-top')[0];
  if( backTop ) {
    var dataElement = backTop.getAttribute('data-element');
    var scrollElement = dataElement ? document.querySelector(dataElement) : window;
    var scrollDuration = parseInt(backTop.getAttribute('data-duration')) || 300, //scroll to top duration
      scrollOffset = parseInt(backTop.getAttribute('data-offset')) || 0, //show back-to-top if scrolling > scrollOffset
      scrolling = false;

    //detect click on back-to-top link
    backTop.addEventListener('click', function(event) {
      event.preventDefault();
      if(!window.requestAnimationFrame) {
        scrollElement.scrollTo(0, 0);
      } else {
        dataElement ? Util.scrollTo(0, scrollDuration, false, scrollElement) : Util.scrollTo(0, scrollDuration);
      }
      //move the focus to the #top-element - don't break keyboard navigation
      Util.moveFocus(document.getElementById(backTop.getAttribute('href').replace('#', '')));
    });

    //listen to the window scroll and update back-to-top visibility
    checkBackToTop();
    if (scrollOffset > 0) {
      scrollElement.addEventListener("scroll", function(event) {
        if( !scrolling ) {
          scrolling = true;
          (!window.requestAnimationFrame) ? setTimeout(function(){checkBackToTop();}, 250) : window.requestAnimationFrame(checkBackToTop);
        }
      });
    }

    function checkBackToTop() {
      var windowTop = scrollElement.scrollTop || document.documentElement.scrollTop;
      if(!dataElement) windowTop = window.scrollY || document.documentElement.scrollTop;
      Util.toggleClass(backTop, 'back-to-top--is-visible', windowTop >= scrollOffset);
      scrolling = false;
    }
  }
}());
function getCookie(name, _default) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : _default;
}

function setCookie(name, value, options) {
    if (!options) {
        options={path: '/'}
    }
    if (name && value) {
        var updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
        for (var optionKey in options) {
            updatedCookie += "; " + optionKey;
            var optionValue = options[optionKey];
            if (optionValue !== true) {
                updatedCookie += "=" + optionValue;
            }
        }
        document.cookie = updatedCookie;
    }
}
// File#: _1_countdown
// Usage: codyhouse.co/license
(function() {
  var CountDown = function(element) {
    this.element = element;
    this.labels = this.element.getAttribute('data-labels') ? this.element.getAttribute('data-labels').split(',') : [];
    this.intervalId;
    //create countdown HTML
    this.createCountDown();
    //store time elements
    this.days = this.element.getElementsByClassName('js-countdown__value--0')[0];
    this.hours = this.element.getElementsByClassName('js-countdown__value--1')[0];
    this.mins = this.element.getElementsByClassName('js-countdown__value--2')[0];
    this.secs = this.element.getElementsByClassName('js-countdown__value--3')[0];
    this.endTime = this.getEndTime();
    //init counter
    this.initCountDown();
  };

  CountDown.prototype.createCountDown = function() {
    var wrapper = document.createElement("div");
    Util.setAttributes(wrapper, {'aria-hidden': 'true', 'class': 'countdown__timer'});

    for(var i = 0; i < 4; i++) {
      var timeItem = document.createElement("span"),
        timeValue = document.createElement("span"),
        timeLabel = document.createElement('span');

      timeItem.setAttribute('class', 'countdown__item');
      timeValue.setAttribute('class', 'countdown__value countdown__value--'+i+' js-countdown__value--'+i);
      timeItem.appendChild(timeValue);

      if( this.labels && this.labels.length > 0 ) {
        timeLabel.textContent = this.labels[i].trim();
        timeLabel.setAttribute('class', 'countdown__label');
        timeItem.appendChild(timeLabel);
      }

      wrapper.appendChild(timeItem);
    }
    // append new content to countdown element
    this.element.insertBefore(wrapper, this.element.firstChild);
    // this.element.appendChild(wrapper);
  };

  CountDown.prototype.getEndTime = function() {
    // get number of remaining seconds
    if(this.element.getAttribute('data-timer')) return Number(this.element.getAttribute('data-timer'))*1000 + new Date().getTime();
    else if(this.element.getAttribute('data-countdown')) return Number(new Date(this.element.getAttribute('data-countdown')).getTime());
  };

  CountDown.prototype.initCountDown = function() {
    var self = this;
    this.intervalId = setInterval(function(){
      self.updateCountDown(false);
    }, 1000);
    this.updateCountDown(true);
  };

  CountDown.prototype.updateCountDown = function(bool) {
    // original countdown function
    // https://gist.github.com/adriennetacke/f5a25c304f1b7b4a6fa42db70415bad2
    var time = parseInt( (this.endTime - new Date().getTime())/1000 ),
      days = 0,
      hours = 0,
      mins = 0,
      seconds = 0;

    if(isNaN(time) || time < 0) {
      clearInterval(this.intervalId);
      this.emitEndEvent();
    } else {
      days = parseInt(time / 86400);
      time = (time % 86400);
      hours = parseInt(time / 3600);
      time = (time % 3600);
      mins = parseInt(time / 60);
      time = (time % 60);
      seconds = parseInt(time);
    }

    // hide days/hours/mins if not available
    if(bool && days == 0) this.days.parentElement.style.display = "none";
    if(bool && days == 0 && hours == 0) this.hours.parentElement.style.display = "none";
    if(bool && days == 0 && hours == 0 && mins == 0) this.mins.parentElement.style.display = "none";

    this.days.textContent = days;
    this.hours.textContent = this.getTimeFormat(hours);
    this.mins.textContent = this.getTimeFormat(mins);
    this.secs.textContent = this.getTimeFormat(seconds);
  };

  CountDown.prototype.getTimeFormat = function(time) {
    return ('0'+ time).slice(-2);
  };

  CountDown.prototype.emitEndEvent = function(time) {
    var event = new CustomEvent('countDownFinished');
    this.element.dispatchEvent(event);
  };

  //initialize the CountDown objects
  var countDown = document.getElementsByClassName('js-countdown');
  if( countDown.length > 0 ) {
    for( var i = 0; i < countDown.length; i++) {
      (function(i){new CountDown(countDown[i]);})(i);
    }
  }
}());
// File#: _1_custom-select
// Usage: codyhouse.co/license
(function() {
    // NOTE: you need the js code only when using the --custom-dropdown variation of the Custom Select component. Default version does nor require JS.

    var CustomSelect = function(element) {
        this.element = element;
        this.select = this.element.getElementsByTagName('select')[0];
        this.optGroups = this.select.getElementsByTagName('optgroup');
        this.options = this.select.getElementsByTagName('option');
        this.selectedOption = getSelectedOptionText(this);
        this.selectId = this.select.getAttribute('id');
        this.trigger = false;
        this.dropdown = false;
        this.customOptions = false;
        this.arrowIcon = this.element.getElementsByTagName('svg');
        this.label = document.querySelector('[for="'+this.selectId+'"]');

        initCustomSelect(this); // init markup
        initCustomSelectEvents(this); // init event listeners
    };

    function initCustomSelect(select) {
        // create the HTML for the custom dropdown element
        select.element.insertAdjacentHTML('beforeend', initButtonSelect(select) + initListSelect(select));

        // save custom elements
        select.dropdown = select.element.getElementsByClassName('js-select__dropdown')[0];
        select.trigger = select.element.getElementsByClassName('js-select__button')[0];
        select.customOptions = select.dropdown.getElementsByClassName('js-select__item');

        // hide default select
        Util.addClass(select.select, 'is-hidden');
        if(select.arrowIcon.length > 0 ) select.arrowIcon[0].style.display = 'none';
    };

    function initCustomSelectEvents(select) {
        // option selection in dropdown
        initSelection(select);

        // click events
        select.trigger.addEventListener('click', function(){
            toggleCustomSelect(select, false);
        });
        if(select.label) {
            // move focus to custom trigger when clicking on <select> label
            select.label.addEventListener('click', function(){
                Util.moveFocus(select.trigger);
            });
        }
        // keyboard navigation
        select.dropdown.addEventListener('keydown', function(event){
            if(event.keyCode && event.keyCode == 38 || event.key && event.key.toLowerCase() == 'arrowup') {
                keyboardCustomSelect(select, 'prev', event);
            } else if(event.keyCode && event.keyCode == 40 || event.key && event.key.toLowerCase() == 'arrowdown') {
                keyboardCustomSelect(select, 'next', event);
            }
        });
    };

    function toggleCustomSelect(select, bool) {
        var ariaExpanded;
        if(bool) {
            ariaExpanded = bool;
        } else {
            ariaExpanded = select.trigger.getAttribute('aria-expanded') == 'true' ? 'false' : 'true';
        }
        select.trigger.setAttribute('aria-expanded', ariaExpanded);
        if(ariaExpanded == 'true') {
            var selectedOption = getSelectedOption(select);
            Util.moveFocus(selectedOption); // fallback if transition is not supported
            select.dropdown.addEventListener('transitionend', function cb(){
                Util.moveFocus(selectedOption);
                select.dropdown.removeEventListener('transitionend', cb);
            });
            placeDropdown(select); // place dropdown based on available space
        }
    };

    function placeDropdown(select) {
        var triggerBoundingRect = select.trigger.getBoundingClientRect();
        Util.toggleClass(select.dropdown, 'select__dropdown--right', (window.innerWidth < triggerBoundingRect.left + select.dropdown.offsetWidth));
        // check if there's enough space up or down
        var moveUp = (window.innerHeight - triggerBoundingRect.bottom) < triggerBoundingRect.top;
        Util.toggleClass(select.dropdown, 'select__dropdown--up', moveUp);
        // check if we need to set a max width
        var maxHeight = moveUp ? triggerBoundingRect.top - 20 : window.innerHeight - triggerBoundingRect.bottom - 20;
        // set max-height based on available space
        select.dropdown.setAttribute('style', 'max-height: '+maxHeight+'px; width: '+triggerBoundingRect.width+'px;');
    };

    function keyboardCustomSelect(select, direction, event) { // navigate custom dropdown with keyboard
        event.preventDefault();
        var index = Util.getIndexInArray(select.customOptions, document.activeElement);
        index = (direction == 'next') ? index + 1 : index - 1;
        if(index < 0) index = select.customOptions.length - 1;
        if(index >= select.customOptions.length) index = 0;
        Util.moveFocus(select.customOptions[index]);
    };

    function initSelection(select) { // option selection
        select.dropdown.addEventListener('click', function(event){
            var option = event.target.closest('.js-select__item');
            if(!option) return;
            selectOption(select, option);
        });
    };

    function selectOption(select, option) {
        if(option.hasAttribute('aria-selected') && option.getAttribute('aria-selected') == 'true') {
            // selecting the same option
            select.trigger.setAttribute('aria-expanded', 'false'); // hide dropdown
        } else {
            var selectedOption = select.dropdown.querySelector('[aria-selected="true"]');
            if(selectedOption) selectedOption.setAttribute('aria-selected', 'false');
            option.setAttribute('aria-selected', 'true');
            select.trigger.getElementsByClassName('js-select__label')[0].textContent = option.textContent;
            select.trigger.setAttribute('aria-expanded', 'false');
            // new option has been selected -> update native <select> element _ arai-label of trigger <button>
            updateNativeSelect(select, option.getAttribute('data-value'));
            updateTriggerAria(select);
        }
        // move focus back to trigger
        select.trigger.focus();
    };

    function updateNativeSelect(select, value) {
        for (var i = 0; i < select.options.length; i++) {
            if (select.options[i].value == value) {
                select.select.selectedIndex = i; // set new value
                select.select.dispatchEvent(new CustomEvent('change')); // trigger change event
                break;
            }
        }
    };

    function updateTriggerAria(select) {
        select.trigger.setAttribute('aria-label', select.options[select.select.selectedIndex].innerHTML+', '+select.label.textContent);
    };

    function getSelectedOptionText(select) {// used to initialize the label of the custom select button
        var label = '';
        if('selectedIndex' in select.select) {
            label = select.options[select.select.selectedIndex].text;
        } else {
            label = select.select.querySelector('option[selected]').text;
        }
        return label;

    };

    function initButtonSelect(select) { // create the button element -> custom select trigger
        // check if we need to add custom classes to the button trigger
        var customClasses = select.element.getAttribute('data-trigger-class') ? ' '+select.element.getAttribute('data-trigger-class') : '';

        var label = select.options[select.select.selectedIndex].innerHTML+', '+select.label.textContent;

        var button = '<button type="button" class="js-select__button select__button'+customClasses+'" aria-label="'+label+'" aria-expanded="false" aria-controls="'+select.selectId+'-dropdown"><span aria-hidden="true" class="js-select__label select__label">'+select.selectedOption+'</span>';
        if(select.arrowIcon.length > 0 && select.arrowIcon[0].outerHTML) {
            var clone = select.arrowIcon[0].cloneNode(true);
            Util.removeClass(clone, 'select__icon');
            button = button +clone.outerHTML;
        }

        return button+'</button>';

    };

    function initListSelect(select) { // create custom select dropdown
        var list = '<div class="js-select__dropdown select__dropdown" aria-describedby="'+select.selectId+'-description" id="'+select.selectId+'-dropdown">';
        list = list + getSelectLabelSR(select);
        if(select.optGroups.length > 0) {
            for(var i = 0; i < select.optGroups.length; i++) {
                var optGroupList = select.optGroups[i].getElementsByTagName('option'),
                    optGroupLabel = '<li><span class="select__item select__item--optgroup">'+select.optGroups[i].getAttribute('label')+'</span></li>';
                list = list + '<ul class="select__list" role="listbox">'+optGroupLabel+getOptionsList(optGroupList) + '</ul>';
            }
        } else {
            list = list + '<ul class="select__list" role="listbox">'+getOptionsList(select.options) + '</ul>';
        }
        return list;
    };

    function getSelectLabelSR(select) {
        if(select.label) {
            return '<p class="sr-only" id="'+select.selectId+'-description">'+select.label.textContent+'</p>'
        } else {
            return '';
        }
    };

    function getOptionsList(options) {
        var list = '';
        for(var i = 0; i < options.length; i++) {
            var selected = options[i].hasAttribute('selected') ? ' aria-selected="true"' : ' aria-selected="false"';
            list = list + '<li><button type="button" class="reset js-select__item select__item select__item--option" role="option" data-value="'+options[i].value+'" '+selected+'>'+options[i].text+'</button></li>';
        };
        return list;
    };

    function getSelectedOption(select) {
        var option = select.dropdown.querySelector('[aria-selected="true"]');
        if(option) return option;
        else return select.dropdown.getElementsByClassName('js-select__item')[0];
    };

    function moveFocusToSelectTrigger(select) {
        if(!document.activeElement.closest('.js-select')) return
        select.trigger.focus();
    };

    function checkCustomSelectClick(select, target) { // close select when clicking outside it
        if( !select.element.contains(target) ) toggleCustomSelect(select, 'false');
    };

    //initialize the CustomSelect objects
    var customSelect = document.getElementsByClassName('js-select');
    if( customSelect.length > 0 ) {
        var selectArray = [];
        for( var i = 0; i < customSelect.length; i++) {
            (function(i){selectArray.push(new CustomSelect(customSelect[i]));})(i);
        }

        // listen for key events
        window.addEventListener('keyup', function(event){
            if( event.keyCode && event.keyCode == 27 || event.key && event.key.toLowerCase() == 'escape' ) {
                // close custom select on 'Esc'
                selectArray.forEach(function(element){
                    moveFocusToSelectTrigger(element); // if focus is within dropdown, move it to dropdown trigger
                    toggleCustomSelect(element, 'false'); // close dropdown
                });
            }
        });
        // close custom select when clicking outside it
        window.addEventListener('click', function(event){
            selectArray.forEach(function(element){
                checkCustomSelectClick(element, event.target);
            });
        });
    }
}());
// File#: _1_expandable-search
// Usage: codyhouse.co/license
(function() {
  var expandableSearch = document.getElementsByClassName('js-expandable-search');
  if(expandableSearch.length > 0) {
    for( var i = 0; i < expandableSearch.length; i++) {
      (function(i){ // if user types in search input, keep the input expanded when focus is lost
        expandableSearch[i].getElementsByClassName('js-expandable-search__input')[0].addEventListener('input', function(event){
          Util.toggleClass(event.target, 'expandable-search__input--has-content', event.target.value.length > 0);
        });
      })(i);
    }
  }
}());
// File#: _1_file-upload
// Usage: codyhouse.co/license
(function() {
  var InputFile = function(element) {
    this.element = element;
    this.input = this.element.getElementsByClassName('file-upload__input')[0];
    this.label = this.element.getElementsByClassName('file-upload__label')[0];
    this.multipleUpload = this.input.hasAttribute('multiple'); // allow for multiple files selection

    // this is the label text element -> when user selects a file, it will be changed from the default value to the name of the file
    this.labelText = this.element.getElementsByClassName('file-upload__text')[0];
    this.initialLabel = this.labelText.textContent;

    initInputFileEvents(this);
  };

  function initInputFileEvents(inputFile) {
    // make label focusable
    inputFile.label.setAttribute('tabindex', '0');
    inputFile.input.setAttribute('tabindex', '-1');

    // move focus from input to label -> this is triggered when a file is selected or the file picker modal is closed
    inputFile.input.addEventListener('focusin', function(event){
      inputFile.label.focus();
    });

    // press 'Enter' key on label element -> trigger file selection
    inputFile.label.addEventListener('keydown', function(event) {
      if( event.keyCode && event.keyCode == 13 || event.key && event.key.toLowerCase() == 'enter') {inputFile.input.click();}
    });

    // file has been selected -> update label text
    inputFile.input.addEventListener('change', function(event){
      updateInputLabelText(inputFile);
    });
  };

  function updateInputLabelText(inputFile) {
    var label = '';
    if(inputFile.input.files && inputFile.input.files.length < 1) {
      label = inputFile.initialLabel; // no selection -> revert to initial label
    } else if(inputFile.multipleUpload && inputFile.input.files && inputFile.input.files.length > 1) {
      label = inputFile.input.files.length+ ' файла(ов)'; // multiple selection -> show number of files
    } else {
      label = inputFile.input.value.split('\\').pop(); // single file selection -> show name of the file
    }
    inputFile.labelText.textContent = label;
  };

  //initialize the InputFile objects
  var inputFiles = document.getElementsByClassName('file-upload');
  if( inputFiles.length > 0 ) {
    for( var i = 0; i < inputFiles.length; i++) {
      (function(i){new InputFile(inputFiles[i]);})(i);
    }
  }
}());
// File#: _1_header
// Usage: codyhouse.co/license
(function() {
  var mainHeader = document.getElementsByClassName('js-header')[0];
  if( mainHeader ) {
    var trigger = mainHeader.getElementsByClassName('js-header__trigger')[0],
      nav = mainHeader.getElementsByClassName('js-header__nav')[0];

    // we'll use these to store the node that needs to receive focus when the mobile menu is closed
    var focusMenu = false;

    //detect click on nav trigger
    trigger.addEventListener("click", function(event) {
      event.preventDefault();
      var ariaExpanded = !Util.hasClass(nav, 'header__nav--is-visible');
      //show nav and update button aria value
      Util.toggleClass(nav, 'header__nav--is-visible', ariaExpanded);
      trigger.setAttribute('aria-expanded', ariaExpanded);
      if(ariaExpanded) { //opening menu -> move focus to first element inside nav
        nav.querySelectorAll('[href], input:not([disabled]), button:not([disabled])')[0].focus();
      } else if(focusMenu) {
        focusMenu.focus();
        focusMenu = false;
      }
    });
    // listen for key events
    window.addEventListener('keyup', function(event){
      // listen for esc key
      if( (event.keyCode && event.keyCode == 27) || (event.key && event.key.toLowerCase() == 'escape' )) {
        // close navigation on mobile if open
        if(trigger.getAttribute('aria-expanded') == 'true' && isVisible(trigger)) {
          focusMenu = trigger; // move focus to menu trigger when menu is close
          trigger.click();
        }
      }
      // listen for tab key
      if( (event.keyCode && event.keyCode == 9) || (event.key && event.key.toLowerCase() == 'tab' )) {
        // close navigation on mobile if open when nav loses focus
        if(trigger.getAttribute('aria-expanded') == 'true' && isVisible(trigger) && !document.activeElement.closest('.js-header')) trigger.click();
      }
    });
  }

  function isVisible(element) {
    return (element.offsetWidth || element.offsetHeight || element.getClientRects().length);
  };
}());
// File#: _1_password
// Usage: codyhouse.co/license
(function() {
    var Password = function(element) {
        this.element = element;
        this.password = this.element.getElementsByClassName('js-password__input')[0];
        this.visibilityBtn = this.element.getElementsByClassName('js-password__btn')[0];
        this.visibilityClass = 'password--text-is-visible';
        this.initPassword();
    };

    Password.prototype.initPassword = function() {
        var self = this;
        //listen to the click on the password btn
        this.visibilityBtn.addEventListener('click', function(event) {
            //if password is in focus -> do nothing if user presses Enter
            if(document.activeElement === self.password) return;
            event.preventDefault();
            self.togglePasswordVisibility();
        });
    };

    Password.prototype.togglePasswordVisibility = function() {
        var makeVisible = !Util.hasClass(this.element, this.visibilityClass);
        //change element class
        Util.toggleClass(this.element, this.visibilityClass, makeVisible);
        //change input type
        (makeVisible) ? this.password.setAttribute('type', 'text') : this.password.setAttribute('type', 'password');
    };

    //initialize the Password objects
    var passwords = document.getElementsByClassName('js-password');
    if( passwords.length > 0 ) {
        for( var i = 0; i < passwords.length; i++) {
            (function(i){new Password(passwords[i]);})(i);
        }
    };
}());
// File#: _1_smooth-scrolling
// Usage: codyhouse.co/license
(function() {
    var SmoothScroll = function(element) {
      this.element = element;
      this.scrollDuration = parseInt(this.element.getAttribute('data-duration')) || 300;
      this.dataElement = this.element.getAttribute('data-element');
      this.scrollElement = this.dataElement ? document.querySelector(this.dataElement) : window;
      this.initScroll();
    };
  
    SmoothScroll.prototype.initScroll = function() {
      var self = this;
  
      //detect click on link
      this.element.addEventListener('click', function(event){
        event.preventDefault();
        var targetId = event.target.closest('.js-smooth-scroll').getAttribute('href').replace('#', ''),
          target = document.getElementById(targetId),
          targetTabIndex = target.getAttribute('tabindex'),
          windowScrollTop = self.scrollElement.scrollTop || document.documentElement.scrollTop;
  
        if(!self.dataElement) windowScrollTop = window.scrollY || document.documentElement.scrollTop;
  
        var scrollElement = self.dataElement ? self.scrollElement : false;
  
        var fixedHeight = self.getFixedElementHeight(); // check if there's a fixed element on the page
        Util.scrollTo(target.getBoundingClientRect().top + windowScrollTop - fixedHeight, self.scrollDuration, function() {
          //move the focus to the target element - don't break keyboard navigation
          Util.moveFocus(target);
          history.pushState(false, false, '#'+targetId);
          self.resetTarget(target, targetTabIndex);
        }, scrollElement);
      });
    };
  
    SmoothScroll.prototype.resetTarget = function(target, tabindex) {
      if( parseInt(target.getAttribute('tabindex')) < 0) {
        target.style.outline = 'none';
        !tabindex && target.removeAttribute('tabindex');
      }	
    };
  
    SmoothScroll.prototype.getFixedElementHeight = function() {
      var fixedElementDelta = parseInt(getComputedStyle(document.documentElement).getPropertyValue('scroll-padding'));
      if(isNaN(fixedElementDelta) ) { // scroll-padding not supported
        fixedElementDelta = 0;
        var fixedElement = document.querySelector(this.element.getAttribute('data-fixed-element'));
        if(fixedElement) fixedElementDelta = parseInt(fixedElement.getBoundingClientRect().height);
      }
      return fixedElementDelta;
    };
    
    //initialize the Smooth Scroll objects
    var smoothScrollLinks = document.getElementsByClassName('js-smooth-scroll');
    if( smoothScrollLinks.length > 0 && !Util.cssSupports('scroll-behavior', 'smooth') && window.requestAnimationFrame) {
      // you need javascript only if css scroll-behavior is not supported
      for( var i = 0; i < smoothScrollLinks.length; i++) {
        (function(i){new SmoothScroll(smoothScrollLinks[i]);})(i);
      }
    }
  }());
// File#: _1_swipe-content
// Usage: codyhouse.co/license
(function() {
  var SwipeContent = function(element) {
    this.element = element;
    this.delta = [false, false];
    this.dragging = false;
    this.intervalId = false;
    initSwipeContent(this);
  };

  function initSwipeContent(content) {
    content.element.addEventListener('mousedown', handleEvent.bind(content));
    content.element.addEventListener('touchstart', handleEvent.bind(content));
  };

  function initDragging(content) {
    //add event listeners
    content.element.addEventListener('mousemove', handleEvent.bind(content));
    content.element.addEventListener('touchmove', handleEvent.bind(content));
    content.element.addEventListener('mouseup', handleEvent.bind(content));
    content.element.addEventListener('mouseleave', handleEvent.bind(content));
    content.element.addEventListener('touchend', handleEvent.bind(content));
  };

  function cancelDragging(content) {
    //remove event listeners
    if(content.intervalId) {
      (!window.requestAnimationFrame) ? clearInterval(content.intervalId) : window.cancelAnimationFrame(content.intervalId);
      content.intervalId = false;
    }
    content.element.removeEventListener('mousemove', handleEvent.bind(content));
    content.element.removeEventListener('touchmove', handleEvent.bind(content));
    content.element.removeEventListener('mouseup', handleEvent.bind(content));
    content.element.removeEventListener('mouseleave', handleEvent.bind(content));
    content.element.removeEventListener('touchend', handleEvent.bind(content));
  };

  function handleEvent(event) {
    switch(event.type) {
      case 'mousedown':
      case 'touchstart':
        startDrag(this, event);
        break;
      case 'mousemove':
      case 'touchmove':
        drag(this, event);
        break;
      case 'mouseup':
      case 'mouseleave':
      case 'touchend':
        endDrag(this, event);
        break;
    }
  };

  function startDrag(content, event) {
    content.dragging = true;
    // listen to drag movements
    initDragging(content);
    content.delta = [parseInt(unify(event).clientX), parseInt(unify(event).clientY)];
    // emit drag start event
    emitSwipeEvents(content, 'dragStart', content.delta, event.target);
  };

  function endDrag(content, event) {
    cancelDragging(content);
    // credits: https://css-tricks.com/simple-swipe-with-vanilla-javascript/
    var dx = parseInt(unify(event).clientX),
      dy = parseInt(unify(event).clientY);

    // check if there was a left/right swipe
    if(content.delta && (content.delta[0] || content.delta[0] === 0)) {
      var s = getSign(dx - content.delta[0]);

      if(Math.abs(dx - content.delta[0]) > 30) {
        (s < 0) ? emitSwipeEvents(content, 'swipeLeft', [dx, dy]) : emitSwipeEvents(content, 'swipeRight', [dx, dy]);
      }

      content.delta[0] = false;
    }
    // check if there was a top/bottom swipe
    if(content.delta && (content.delta[1] || content.delta[1] === 0)) {
    	var y = getSign(dy - content.delta[1]);

    	if(Math.abs(dy - content.delta[1]) > 30) {
      	(y < 0) ? emitSwipeEvents(content, 'swipeUp', [dx, dy]) : emitSwipeEvents(content, 'swipeDown', [dx, dy]);
      }

      content.delta[1] = false;
    }
    // emit drag end event
    emitSwipeEvents(content, 'dragEnd', [dx, dy]);
    content.dragging = false;
  };

  function drag(content, event) {
    if(!content.dragging) return;
    // emit dragging event with coordinates
    (!window.requestAnimationFrame)
      ? content.intervalId = setTimeout(function(){emitDrag.bind(content, event);}, 250)
      : content.intervalId = window.requestAnimationFrame(emitDrag.bind(content, event));
  };

  function emitDrag(event) {
    emitSwipeEvents(this, 'dragging', [parseInt(unify(event).clientX), parseInt(unify(event).clientY)]);
  };

  function unify(event) {
    // unify mouse and touch events
    return event.changedTouches ? event.changedTouches[0] : event;
  };

  function emitSwipeEvents(content, eventName, detail, el) {
    var trigger = false;
    if(el) trigger = el;
    // emit event with coordinates
    var event = new CustomEvent(eventName, {detail: {x: detail[0], y: detail[1], origin: trigger}});
    content.element.dispatchEvent(event);
  };

  function getSign(x) {
    if(!Math.sign) {
      return ((x > 0) - (x < 0)) || +x;
    } else {
      return Math.sign(x);
    }
  };

  window.SwipeContent = SwipeContent;

  //initialize the SwipeContent objects
  var swipe = document.getElementsByClassName('js-swipe-content');
  if( swipe.length > 0 ) {
    for( var i = 0; i < swipe.length; i++) {
      (function(i){new SwipeContent(swipe[i]);})(i);
    }
  }
}());
// File#: _1_table
// Usage: codyhouse.co/license
(function() {
    function initTable(table) {
        checkTableLayour(table); // switch from a collapsed to an expanded layout
        Util.addClass(table, 'table--loaded'); // show table

        // custom event emitted when window is resized
        table.addEventListener('update-table', function(event){
            checkTableLayour(table);
        });
    };

    function checkTableLayour(table) {
        var layout = getComputedStyle(table, ':before').getPropertyValue('content').replace(/\'|"/g, '');
        Util.toggleClass(table, tableExpandedLayoutClass, layout != 'collapsed');
    };

    var tables = document.getElementsByClassName('js-table'),
        tableExpandedLayoutClass = 'table--expanded';
    if( tables.length > 0 ) {
        var j = 0;
        for( var i = 0; i < tables.length; i++) {
            var beforeContent = getComputedStyle(tables[i], ':before').getPropertyValue('content');
            if(beforeContent && beforeContent !='' && beforeContent !='none') {
                (function(i){initTable(tables[i]);})(i);
                j = j + 1;
            } else {
                Util.addClass(tables[i], 'table--loaded');
            }
        }

        if(j > 0) {
            var resizingId = false,
                customEvent = new CustomEvent('update-table');
            window.addEventListener('resize', function(event){
                clearTimeout(resizingId);
                resizingId = setTimeout(doneResizing, 300);
            });

            function doneResizing() {
                for( var i = 0; i < tables.length; i++) {
                    (function(i){tables[i].dispatchEvent(customEvent)})(i);
                };
            };
        }
    }
}());
function loadImage(event, input) {
    var output = document.getElementById(input.getAttribute('for'));
    loadFile(event, input);

    output.classList.add('img-thumbnail');
    output.classList.add('mb-3');
    output.classList.remove('hide');
    output.src = URL.createObjectURL(event.target.files[0]);
}

function loadFile(event, input) {
    console.log(event);
    console.log(input);
    document.querySelectorAll('.custom-file-label[for="' + input.id + '"]').forEach(function (value) {
        console.log(value);
        value.innerHTML = event.target.files[0].name
    });
}

function loadingButton(btn) {
    if (btn.parentElement.checkValidity()) {
        btn.innerHTML =
            '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ' +
            'Загрузка...'
    }
}
var del_data = {};
function del_selector(elem) {
    var f = elem.getAttribute('for');
    var form = document.getElementById(f);
    if (elem.checked) {
        del_data[f] = form.innerHTML;
        form.innerHTML = '';
        elem.name = elem.getAttribute('_name');
    } else {
        form.innerHTML = del_data[f];
        elem.name = '';
    }
}

document.querySelectorAll('button.btn[type=submit]').forEach(function (elem) {
    elem.setAttribute('onclick', "loadingButton(this)")
});

// document.querySelectorAll("label:not(.custom-file-label)").forEach(function (elem) {
//     var for_id = elem.getAttribute('for');
//     if (for_id && document.getElementById(for_id).required) {
//         elem.innerHTML += ' <span class="color-error">*</span>'
//     }
// });

// File#: _1_vertical-timeline
// Usage: codyhouse.co/license
(function() {
    var VTimeline = function(element) {
      this.element = element;
      this.sections = this.element.getElementsByClassName('js-v-timeline__section');
      this.animate = this.element.getAttribute('data-animation') && this.element.getAttribute('data-animation') == 'on' ? true : false;
      this.animationClass = 'v-timeline__section--animate';
      this.animationDelta = '-150px';
      initVTimeline(this);
    };
  
    function initVTimeline(element) {
      if(!element.animate) return;
      for(var i = 0; i < element.sections.length; i++) {
        var observer = new IntersectionObserver(vTimelineCallback.bind(element, i),
        {rootMargin: "0px 0px "+element.animationDelta+" 0px"});
        observer.observe(element.sections[i]);
      }
    };
  
    function vTimelineCallback(index, entries, observer) {
      if(entries[0].isIntersecting) {
        Util.addClass(this.sections[index], this.animationClass);
        observer.unobserve(this.sections[index]);
      } 
    };
  
    //initialize the VTimeline objects
    var timelines = document.querySelectorAll('.js-v-timeline'),
      intersectionObserverSupported = ('IntersectionObserver' in window && 'IntersectionObserverEntry' in window && 'intersectionRatio' in window.IntersectionObserverEntry.prototype),
      reducedMotion = Util.osHasReducedMotion();
    if( timelines.length > 0) {
      for( var i = 0; i < timelines.length; i++) {
        if(intersectionObserverSupported && !reducedMotion) (function(i){new VTimeline(timelines[i]);})(i);
        else timelines[i].removeAttribute('data-animation');
      }
    }
  }());
// File#: _2_flexi-header
// Usage: codyhouse.co/license
(function() {
  var flexHeader = document.getElementsByClassName('js-f-header');
  if(flexHeader.length > 0) {
    var menuTrigger = flexHeader[0].getElementsByClassName('js-anim-menu-btn')[0],
      firstFocusableElement = getMenuFirstFocusable();

    // we'll use these to store the node that needs to receive focus when the mobile menu is closed
    var focusMenu = false;

    menuTrigger.addEventListener('anim-menu-btn-clicked', function(event){ // toggle menu visibility an small devices
      Util.toggleClass(document.getElementsByClassName('f-header__nav')[0], 'f-header__nav--is-visible', event.detail);
      menuTrigger.setAttribute('aria-expanded', event.detail);
      if(event.detail) firstFocusableElement.focus(); // move focus to first focusable element
      else if(focusMenu) {
        focusMenu.focus();
        focusMenu = false;
      }
    });

    // listen for key events
    window.addEventListener('keyup', function(event){
      // listen for esc key
      if( (event.keyCode && event.keyCode == 27) || (event.key && event.key.toLowerCase() == 'escape' )) {
        // close navigation on mobile if open
        if(menuTrigger.getAttribute('aria-expanded') == 'true' && isVisible(menuTrigger)) {
          focusMenu = menuTrigger; // move focus to menu trigger when menu is close
          menuTrigger.click();
        }
      }
      // listen for tab key
      if( (event.keyCode && event.keyCode == 9) || (event.key && event.key.toLowerCase() == 'tab' )) {
        // close navigation on mobile if open when nav loses focus
        if(menuTrigger.getAttribute('aria-expanded') == 'true' && isVisible(menuTrigger) && !document.activeElement.closest('.js-f-header')) menuTrigger.click();
      }
    });

    function getMenuFirstFocusable() {
      var focusableEle = flexHeader[0].getElementsByClassName('f-header__nav')[0].querySelectorAll('[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), iframe, object, embed, [tabindex]:not([tabindex="-1"]), [contenteditable], audio[controls], video[controls], summary'),
        firstFocusable = false;
      for(var i = 0; i < focusableEle.length; i++) {
        if( focusableEle[i].offsetWidth || focusableEle[i].offsetHeight || focusableEle[i].getClientRects().length ) {
          firstFocusable = focusableEle[i];
          break;
        }
      }

      return firstFocusable;
    };

    function isVisible(element) {
      return (element.offsetWidth || element.offsetHeight || element.getClientRects().length);
    };
  }
}());
// File#: _2_slideshow
// Usage: codyhouse.co/license
(function() {
  var Slideshow = function(opts) {
    this.options = slideshowAssignOptions(Slideshow.defaults , opts);
    this.element = this.options.element;
    this.items = this.element.getElementsByClassName('js-slideshow__item');
    this.controls = this.element.getElementsByClassName('js-slideshow__control');
    this.selectedSlide = 0;
    this.autoplayId = false;
    this.autoplayPaused = false;
    this.navigation = false;
    this.navCurrentLabel = false;
    this.ariaLive = false;
    this.moveFocus = false;
    this.animating = false;
    this.supportAnimation = Util.cssSupports('transition');
    this.animationOff = (!Util.hasClass(this.element, 'slideshow--transition-fade') && !Util.hasClass(this.element, 'slideshow--transition-slide'));
    this.animatingClass = 'slideshow--is-animating';
    initSlideshow(this);
    initSlideshowEvents(this);
    initAnimationEndEvents(this);
  };

  Slideshow.prototype.showNext = function() {
    showNewItem(this, this.selectedSlide + 1, 'next');
  };

  Slideshow.prototype.showPrev = function() {
    showNewItem(this, this.selectedSlide - 1, 'prev');
  };

  Slideshow.prototype.showItem = function(index) {
    showNewItem(this, index, false);
  };

  Slideshow.prototype.startAutoplay = function() {
    var self = this;
    if(this.options.autoplay && !this.autoplayId && !this.autoplayPaused) {
      self.autoplayId = setInterval(function(){
        self.showNext();
      }, self.options.autoplayInterval);
    }
  };

  Slideshow.prototype.pauseAutoplay = function() {
    var self = this;
    if(this.options.autoplay) {
      clearInterval(self.autoplayId);
      self.autoplayId = false;
    }
  };

  function slideshowAssignOptions(defaults, opts) {
    // initialize the object options
    var mergeOpts = {};
    mergeOpts.element = (typeof opts.element !== "undefined") ? opts.element : defaults.element;
    mergeOpts.navigation = (typeof opts.navigation !== "undefined") ? opts.navigation : defaults.navigation;
    mergeOpts.autoplay = (typeof opts.autoplay !== "undefined") ? opts.autoplay : defaults.autoplay;
    mergeOpts.autoplayInterval = (typeof opts.autoplayInterval !== "undefined") ? opts.autoplayInterval : defaults.autoplayInterval;
    mergeOpts.swipe = (typeof opts.swipe !== "undefined") ? opts.swipe : defaults.swipe;
    return mergeOpts;
  };

  function initSlideshow(slideshow) { // basic slideshow settings
    // if no slide has been selected -> select the first one
    if(slideshow.element.getElementsByClassName('slideshow__item--selected').length < 1) Util.addClass(slideshow.items[0], 'slideshow__item--selected');
    slideshow.selectedSlide = Util.getIndexInArray(slideshow.items, slideshow.element.getElementsByClassName('slideshow__item--selected')[0]);
    // create an element that will be used to announce the new visible slide to SR
    var srLiveArea = document.createElement('div');
    Util.setAttributes(srLiveArea, {'class': 'sr-only js-slideshow__aria-live', 'aria-live': 'polite', 'aria-atomic': 'true'});
    slideshow.element.appendChild(srLiveArea);
    slideshow.ariaLive = srLiveArea;
  };

  function initSlideshowEvents(slideshow) {
    // if slideshow navigation is on -> create navigation HTML and add event listeners
    if(slideshow.options.navigation) {
      var navigation = document.createElement('ol'),
        navChildren = '';

      navigation.setAttribute('class', 'slideshow__navigation');
      for(var i = 0; i < slideshow.items.length; i++) {
        var className = (i == slideshow.selectedSlide) ? 'class="slideshow__nav-item slideshow__nav-item--selected js-slideshow__nav-item"' :  'class="slideshow__nav-item js-slideshow__nav-item"',
          navCurrentLabel = (i == slideshow.selectedSlide) ? '<span class="sr-only js-slideshow__nav-current-label">Current Item</span>' : '';
        navChildren = navChildren + '<li '+className+'><button class="reset"><span class="sr-only">'+ (i+1) + '</span>'+navCurrentLabel+'</button></li>';
      }

      navigation.innerHTML = navChildren;
      slideshow.navCurrentLabel = navigation.getElementsByClassName('js-slideshow__nav-current-label')[0];
      slideshow.element.appendChild(navigation);
      slideshow.navigation = slideshow.element.getElementsByClassName('js-slideshow__nav-item');

      navigation.addEventListener('click', function(event){
        navigateSlide(slideshow, event, true);
      });
      navigation.addEventListener('keyup', function(event){
        navigateSlide(slideshow, event, (event.key.toLowerCase() == 'enter'));
      });
    }
    // slideshow arrow controls
    if(slideshow.controls.length > 0) {
      slideshow.controls[0].addEventListener('click', function(event){
        event.preventDefault();
        slideshow.showPrev();
        updateAriaLive(slideshow);
      });
      slideshow.controls[1].addEventListener('click', function(event){
        event.preventDefault();
        slideshow.showNext();
        updateAriaLive(slideshow);
      });
    }
    // swipe events
    if(slideshow.options.swipe) {
      //init swipe
      new SwipeContent(slideshow.element);
      slideshow.element.addEventListener('swipeLeft', function(event){
        slideshow.showNext();
      });
      slideshow.element.addEventListener('swipeRight', function(event){
        slideshow.showPrev();
      });
    }
    // autoplay
    if(slideshow.options.autoplay) {
      slideshow.startAutoplay();
      // pause autoplay if user is interacting with the slideshow
      slideshow.element.addEventListener('mouseenter', function(event){
        slideshow.pauseAutoplay();
        slideshow.autoplayPaused = true;
      });
      slideshow.element.addEventListener('focusin', function(event){
        slideshow.pauseAutoplay();
        slideshow.autoplayPaused = true;
      });
      slideshow.element.addEventListener('mouseleave', function(event){
        slideshow.autoplayPaused = false;
        slideshow.startAutoplay();
      });
      slideshow.element.addEventListener('focusout', function(event){
        slideshow.autoplayPaused = false;
        slideshow.startAutoplay();
      });
    }
    // detect if external buttons control the slideshow
    var slideshowId = slideshow.element.getAttribute('id');
    if(slideshowId) {
      var externalControls = document.querySelectorAll('[data-controls="'+slideshowId+'"]');
      for(var i = 0; i < externalControls.length; i++) {
        (function(i){externalControlSlide(slideshow, externalControls[i]);})(i);
      }
    }
    // custom event to trigger selection of a new slide element
    slideshow.element.addEventListener('selectNewItem', function(event){
      if(event.detail) showNewItem(slideshow, event.detail - 1, false);
    });
  };

  function navigateSlide(slideshow, event, keyNav) {
    // user has interacted with the slideshow navigation -> update visible slide
    var target = ( Util.hasClass(event.target, 'js-slideshow__nav-item') ) ? event.target : event.target.closest('.js-slideshow__nav-item');
    if(keyNav && target && !Util.hasClass(target, 'slideshow__nav-item--selected')) {
      slideshow.showItem(Util.getIndexInArray(slideshow.navigation, target));
      slideshow.moveFocus = true;
      updateAriaLive(slideshow);
    }
  };

  function initAnimationEndEvents(slideshow) {
    // remove animation classes at the end of a slide transition
    for( var i = 0; i < slideshow.items.length; i++) {
      (function(i){
        slideshow.items[i].addEventListener('animationend', function(){resetAnimationEnd(slideshow, slideshow.items[i]);});
        slideshow.items[i].addEventListener('transitionend', function(){resetAnimationEnd(slideshow, slideshow.items[i]);});
      })(i);
    }
  };

  function resetAnimationEnd(slideshow, item) {
    setTimeout(function(){ // add a delay between the end of animation and slideshow reset - improve animation performance
      if(Util.hasClass(item,'slideshow__item--selected')) {
        if(slideshow.moveFocus) Util.moveFocus(item);
        emitSlideshowEvent(slideshow, 'newItemVisible', slideshow.selectedSlide);
        slideshow.moveFocus = false;
      }
      Util.removeClass(item, 'slideshow__item--slide-out-left slideshow__item--slide-out-right slideshow__item--slide-in-left slideshow__item--slide-in-right');
      item.removeAttribute('aria-hidden');
      slideshow.animating = false;
      Util.removeClass(slideshow.element, slideshow.animatingClass);
    }, 100);
  };

  function showNewItem(slideshow, index, bool) {
    if(slideshow.animating && slideshow.supportAnimation) return;
    slideshow.animating = true;
    Util.addClass(slideshow.element, slideshow.animatingClass);
    if(index < 0) index = slideshow.items.length - 1;
    else if(index >= slideshow.items.length) index = 0;
    var exitItemClass = getExitItemClass(bool, slideshow.selectedSlide, index);
    var enterItemClass = getEnterItemClass(bool, slideshow.selectedSlide, index);
    // transition between slides
    if(!slideshow.animationOff) Util.addClass(slideshow.items[slideshow.selectedSlide], exitItemClass);
    Util.removeClass(slideshow.items[slideshow.selectedSlide], 'slideshow__item--selected');
    slideshow.items[slideshow.selectedSlide].setAttribute('aria-hidden', 'true'); //hide to sr element that is exiting the viewport
    if(slideshow.animationOff) {
      Util.addClass(slideshow.items[index], 'slideshow__item--selected');
    } else {
      Util.addClass(slideshow.items[index], enterItemClass+' slideshow__item--selected');
    }
    // reset slider navigation appearance
    resetSlideshowNav(slideshow, index, slideshow.selectedSlide);
    slideshow.selectedSlide = index;
    // reset autoplay
    slideshow.pauseAutoplay();
    slideshow.startAutoplay();
    // reset controls/navigation color themes
    resetSlideshowTheme(slideshow, index);
    // emit event
    emitSlideshowEvent(slideshow, 'newItemSelected', slideshow.selectedSlide);
    if(slideshow.animationOff) {
      slideshow.animating = false;
      Util.removeClass(slideshow.element, slideshow.animatingClass);
    }
  };

  function getExitItemClass(bool, oldIndex, newIndex) {
    var className = '';
    if(bool) {
      className = (bool == 'next') ? 'slideshow__item--slide-out-right' : 'slideshow__item--slide-out-left';
    } else {
      className = (newIndex < oldIndex) ? 'slideshow__item--slide-out-left' : 'slideshow__item--slide-out-right';
    }
    return className;
  };

  function getEnterItemClass(bool, oldIndex, newIndex) {
    var className = '';
    if(bool) {
      className = (bool == 'next') ? 'slideshow__item--slide-in-right' : 'slideshow__item--slide-in-left';
    } else {
      className = (newIndex < oldIndex) ? 'slideshow__item--slide-in-left' : 'slideshow__item--slide-in-right';
    }
    return className;
  };

  function resetSlideshowNav(slideshow, newIndex, oldIndex) {
    if(slideshow.navigation) {
      Util.removeClass(slideshow.navigation[oldIndex], 'slideshow__nav-item--selected');
      Util.addClass(slideshow.navigation[newIndex], 'slideshow__nav-item--selected');
      slideshow.navCurrentLabel.parentElement.removeChild(slideshow.navCurrentLabel);
      slideshow.navigation[newIndex].getElementsByTagName('button')[0].appendChild(slideshow.navCurrentLabel);
    }
  };

  function resetSlideshowTheme(slideshow, newIndex) {
    var dataTheme = slideshow.items[newIndex].getAttribute('data-theme');
    if(dataTheme) {
      if(slideshow.navigation) slideshow.navigation[0].parentElement.setAttribute('data-theme', dataTheme);
      if(slideshow.controls[0]) slideshow.controls[0].parentElement.setAttribute('data-theme', dataTheme);
    } else {
      if(slideshow.navigation) slideshow.navigation[0].parentElement.removeAttribute('data-theme');
      if(slideshow.controls[0]) slideshow.controls[0].parentElement.removeAttribute('data-theme');
    }
  };

  function emitSlideshowEvent(slideshow, eventName, detail) {
    var event = new CustomEvent(eventName, {detail: detail});
    slideshow.element.dispatchEvent(event);
  };

  function updateAriaLive(slideshow) {
    slideshow.ariaLive.innerHTML = 'Item '+(slideshow.selectedSlide + 1)+' of '+slideshow.items.length;
  };

  function externalControlSlide(slideshow, button) { // control slideshow using external element
    button.addEventListener('click', function(event){
      var index = button.getAttribute('data-index');
      if(!index) return;
      event.preventDefault();
      showNewItem(slideshow, index - 1, false);
    });
  };

  Slideshow.defaults = {
    element : '',
    navigation : true,
    autoplay : false,
    autoplayInterval: 5000,
    swipe: false
  };

  window.Slideshow = Slideshow;

  //initialize the Slideshow objects
  var slideshows = document.getElementsByClassName('js-slideshow');
  if( slideshows.length > 0 ) {
    for( var i = 0; i < slideshows.length; i++) {
      (function(i){
        var navigation = (slideshows[i].getAttribute('data-navigation') && slideshows[i].getAttribute('data-navigation') == 'off') ? false : true,
          autoplay = (slideshows[i].getAttribute('data-autoplay') && slideshows[i].getAttribute('data-autoplay') == 'on') ? true : false,
          autoplayInterval = (slideshows[i].getAttribute('data-autoplay-interval')) ? slideshows[i].getAttribute('data-autoplay-interval') : 5000,
          swipe = (slideshows[i].getAttribute('data-swipe') && slideshows[i].getAttribute('data-swipe') == 'on') ? true : false;
        new Slideshow({element: slideshows[i], navigation: navigation, autoplay : autoplay, autoplayInterval : autoplayInterval, swipe : swipe});
      })(i);
    }
  }
}());