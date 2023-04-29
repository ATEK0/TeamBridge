  // Define the duration of the animation in milliseconds
  const duration = 5000; // 5 seconds
  
  // Get the timer element
  const timer = document.querySelector('.timer');
  
  // Define the starting and ending width values
  const startWidth = 100;
  const endWidth = 0;
  

  const element = document.querySelector('.flash');
  // Define the animation function
  function animateWidth() {
    element.classList.add('slide-in');
    let currentWidth = startWidth;
    const interval = setInterval(() => {
      currentWidth -= (startWidth - endWidth) / (duration / 10);
      timer.style.width = currentWidth + '%';
      if (currentWidth <= endWidth) {
        element.classList.remove('slide-in');
        element.classList.add('slide-out');
        clearInterval(interval);
        setInterval(() => {
            element.remove();
        }, 450)
      }
    }, 10);

  }
  const toastEl = document.querySelector('.toast');
  const toast = new bootstrap.Toast(toastEl);
  toast.show();
  



//   <div class="flash position-fixed mb-3 ml-3 mr-3 mt-1 bg-light" style="right: 0;border-radius:0px 0px 20px 20px;">
//               <div class="border-bottom border-left border-right border-light bg-{{category}} bg-gradient text-center" style="border-radius:0px 0px 20px 20px;width:20rem;border-width: 3px !important;">
//                 <div class="timer border-bottom border-light bg-{{category}} bg-gradient" style="border-width: 3px !important;"></div>  
//                   {% if category == 'danger'%}
//                   <div class="flash-title font-weight-bold pl-2 pb-0 pr-2 pt-0 text-light">ERROR</div>
//                   {% else %}
//                   <div class="flash-title font-weight-bold pl-2 pb-0 pr-2 pt-0 text-light">{{category.upper()}}</div>
//                   {% endif %}
                  
//                   <div class="flash-content text-break pl-2 pb-2 pr-2 pt-0 text-light">{{message}}</div>
//               </div>
//             </div>