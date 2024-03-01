let solnce = document.getElementById("sun");
solnce.onclick = function (){
    let them = document.getElementById("them");
    if (them.getAttribute("href") == "regzayavki.css") {
        them.href = "dark.css";
        document.getElementById('datesimg').src="img/Bcalendar.png";
        document.getElementById('settingimg').src="img/Blackgear.png";
        document.getElementById('rezultatimg').src="img/Bmedal.png";
        document.getElementById('historyimg').src="img/Bclock.png";
        document.getElementById("registerimg").src = 'img/Blackpenc.png';
        document.getElementById("mainpageimg").src = 'img/Blackhouse.png';
        document.getElementById('l-tip').src="img/shortcuticon.png";
        document.getElementById('sunw').src="img/Sunwhite.png";
        document.getElementById('chatblack').src="img/Chatwhite.png";
    }
    else{
        them.href = "regzayavki.css";
        document.getElementById('rezultatimg').src="img/Medal.png";
        document.getElementById('datesimg').src="img/Calendar.png";
        document.getElementById('settingimg').src="img/Gear.png";
        document.getElementById('historyimg').src="img/ClockClockwise.png";
        document.getElementById("registerimg").src = 'img/NotePencil.png';
        document.getElementById('l-tip').src='img/logoolimp.jpg';
        document.getElementById("mainpageimg").src = 'img/Vector.png';
        document.getElementById('sunw').src="img/sun.png";
        document.getElementById('chatblack').src="img/Chatblack.png";
    }
}
