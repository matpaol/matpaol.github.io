const clock=document.getElementById('clock');
if(clock){const update=()=>clock.textContent=new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Brussels',hour12:false,hour:'2-digit',minute:'2-digit',second:'2-digit'}).format(new Date());update();setInterval(update,1000)}
const copy=document.getElementById('copy-email'),toast=document.getElementById('toast');
let resetCopy;
copy?.addEventListener('click',async()=>{try{await navigator.clipboard.writeText('paolini134@gmail.com');copy.textContent='Copied';toast.textContent='Email copied';toast.classList.add('show');clearTimeout(resetCopy);resetCopy=setTimeout(()=>{copy.textContent='Copy email';toast.classList.remove('show')},2500)}catch{toast.textContent='Email: paolini134@gmail.com';toast.classList.add('show')}});
const filters=[...document.querySelectorAll('[data-filter]')],cards=[...document.querySelectorAll('[data-category]')];
filters.forEach(button=>button.addEventListener('click',()=>{filters.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));let count=0;cards.forEach(card=>{card.hidden=button.dataset.filter!=='All'&&card.dataset.category!==button.dataset.filter;if(!card.hidden)count++});document.querySelector('.filter-status').textContent=`${count} projects`;document.querySelector('.empty-state').hidden=count!==0}));
document.querySelectorAll('[data-video]').forEach(button=>button.addEventListener('click',()=>{const iframe=document.createElement('iframe');iframe.src=`https://www.youtube-nocookie.com/embed/${button.dataset.video}?autoplay=1`;iframe.title='Tentacle Robotic Gripper — project demo';iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';iframe.allowFullscreen=true;button.parentElement.replaceChildren(iframe)}));
const cv=document.getElementById('cv-dialog');
document.querySelector('[data-cv]')?.addEventListener('click',()=>cv.showModal());
document.querySelectorAll('[data-close]').forEach(button=>button.addEventListener('click',()=>button.closest('dialog')?.close()));
const nerdDialog=document.getElementById('nerd-dialog');
document.getElementById('nerd-trigger')?.addEventListener('click',()=>nerdDialog?.showModal());
document.querySelectorAll('[data-map]').forEach(button=>button.addEventListener('click',()=>{
 const frame=document.createElement('iframe');frame.src=button.dataset.map;frame.title=button.dataset.title;frame.setAttribute('sandbox','allow-scripts');frame.setAttribute('loading','lazy');button.parentElement.replaceChildren(frame);
}));
