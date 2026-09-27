const messages=document.getElementById("messages");
const form=document.getElementById("chatForm"),input=document.getElementById("input");
const statusEl=document.getElementById("status"),emotionEl=document.getElementById("emotion");
const avatar=document.getElementById("avatar"),mouth=document.getElementById("mouth");
let ws;

function addMessage(role,text){
  const d=document.createElement("div");d.className=`message ${role}`;d.textContent=text;
  messages.appendChild(d);messages.scrollTop=messages.scrollHeight;
}
function setEmotion(name){
  avatar.className=`avatar ${name}`;emotionEl.textContent=`Emotion: ${name}`;
  const open={neutral:15,happy:24,sad:12,angry:17,surprised:32}[name]??15;
  mouth.style.height=`${open}px`;
}
function connect(){
  const p=location.protocol==="https:"?"wss":"ws";
  ws=new WebSocket(`${p}://${location.host}/ws`);
  ws.onopen=()=>statusEl.textContent="已连接";
  ws.onclose=()=>{statusEl.textContent="连接断开，正在重连...";setTimeout(connect,1500)};
  ws.onerror=()=>statusEl.textContent="连接错误";
  ws.onmessage=e=>{
    const m=JSON.parse(e.data);
    if(m.type==="system")addMessage("system",m.data.message);
    if(m.type==="thinking")statusEl.textContent=m.data.value?"芙酱正在思考...":"已连接";
    if(m.type==="message"){addMessage("assistant",m.data.text);setEmotion(m.data.emotion)}
    if(m.type==="emotion")setEmotion(m.data.emotion);
    if(m.type==="audio"){const a=new Audio(m.data.url);a.play().catch(()=>{})}
    if(m.type==="error")addMessage("system","错误："+m.data.message);
  };
}
form.addEventListener("submit",e=>{
  e.preventDefault();const text=input.value.trim();
  if(!text||!ws||ws.readyState!==WebSocket.OPEN)return;
  addMessage("user",text);ws.send(JSON.stringify({type:"chat",message:text}));
  input.value="";input.focus();
});
connect();
