var socket = io();
    document.getElementById('forward').addEventListener('click',(e)=>{
    socket.emit('movement_command','forward')
})
    document.getElementById('for-left').addEventListener('click',(e)=>{
    socket.emit('movement_command','for-left')
})
    document.getElementById('for-right').addEventListener('click',(e)=>{
    socket.emit('movement_command','for-right')
})
    document.getElementById('left').addEventListener('click',(e)=>{
    socket.emit('movement_command','left')
})
    document.getElementById('stop').addEventListener('click',(e)=>{
    socket.emit('movement_command','stop')
})
    document.getElementById('right').addEventListener('click',(e)=>{
    socket.emit('movement_command','right')
})
    document.getElementById('backward').addEventListener('click',(e)=>{
    socket.emit('movement_command','backward')
})
    setInterval(function() {
        socket.emit('sensor_data');
    }, 2000) 
    socket.on('sensor_data', (data) => {
         
        document.getElementById('sensor_data').innerText = data;
        console.log("Received data: " + data);

    });
    socket.on('connect',(data)=>{
        console.log(data)
    })
