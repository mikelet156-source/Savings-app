<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SaveTogether - Uganda</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-purple-600 to-green-500 min-h-screen p-4">
<div class="max-w-md mx-auto bg-white rounded-3xl shadow-2xl p-6 mt-10">
<h1 class="text-3xl font-bold text-center text-purple-700">💰 SaveTogether</h1>
<p class="text-center text-gray-500 mb-6">Uganda Group Savings - LIVE DB</p>

<div class="bg-purple-50 p-4 rounded-2xl mb-4">
<p class="text-sm text-gray-600">Total Real Savings (Database)</p>
<h2 id="balance" class="text-3xl font-bold">Loading...</h2>
</div>

<input id="phone" placeholder="MTN 075XXXXXXX" class="w-full p-3 border rounded-xl mb-3" value="0754307701">
<input id="amount" type="number" placeholder="Amount UGX" class="w-full p-3 border rounded-xl mb-3" value="8000">
<div class="grid grid-cols-2 gap-3">
<button onclick="realDeposit()" class="bg-purple-600 text-white p-3 rounded-xl font-bold">Real Deposit</button>
<button onclick="realWithdraw()" class="bg-green-600 text-white p-3 rounded-xl font-bold">Real Withdraw</button>
</div>

<div id="msg" class="mt-4 text-center text-sm font-bold"></div>
<h3 class="font-bold mt-6 mb-2">Recent Activity (from DB)</h3>
<ul id="history" class="text-sm text-gray-600"></ul>

<div class="mt-6 bg-yellow-50 p-3 rounded-xl text-xs">
<b>To enable REAL MTN Mobile Money:</b><br>
1. Go to momodeveloper.mtn.com<br>
2. Register for Collections API<br>
3. Get API Key<br>
4. Tell me your API key, I will connect it
</div>
</div>

<script>
const API = "https://savings-app-7rr5.onrender.com";
async function loadBalance(){
 let r=await fetch(API+"/balance");
 let d=await r.json();
 document.getElementById('balance').innerText="UGX "+(d.balance||0).toLocaleString();
 let h=document.getElementById('history'); h.innerHTML="";
 (d.transactions||[]).forEach(t=>{
  let li=document.createElement('li');
  li.innerText=t.created_at?.slice(11,19)+" - "+t.type+" UGX "+t.amount+" ("+t.phone+")";
  h.appendChild(li);
 });
}
async function realDeposit(){
 let phone=document.getElementById('phone').value;
 let amount=Number(document.getElementById('amount').value);
 document.getElementById('msg').innerText="Saving to real database...";
 let r=await fetch(API+"/deposit",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone,amount})});
 let d=await r.json();
 document.getElementById('msg').innerText="✅ "+d.message;
 loadBalance();
}
async function realWithdraw(){
 let phone=document.getElementById('phone').value;
 let amount=Number(document.getElementById('amount').value);
 let r=await fetch(API+"/withdraw",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone,amount})});
 let d=await r.json();
 document.getElementById('msg').innerText=d.message||"Done";
 loadBalance();
}
loadBalance();
setInterval(loadBalance, 3000);
</script>
</body>
</html>
