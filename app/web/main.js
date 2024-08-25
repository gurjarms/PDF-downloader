// Check internet connectivity after 3 seconds on page load
window.onload = () => {
      setTimeout(checkInternet, 3000);
};

function checkInternet() {
      if (!navigator.onLine) {
            alert('You are offline');
      }
}

document.addEventListener("contextmenu", (event) => {
      event.preventDefault();
})
let state = 0

// Disable  key combinations for security
document.onkeydown = (e) => {
      const forbiddenKeys = [
            { key: 'F12' },
            { key: 'I', ctrlKey: true, shiftKey: true },
            { key: 'C', ctrlKey: true, shiftKey: true },
            { key: 'J', ctrlKey: true, shiftKey: true },
            { key: 'N', ctrlKey: true, shiftKey: true },
            { key: 'P', ctrlKey: true, shiftKey: true },
            { key: 'R', ctrlKey: true, shiftKey: true },
            { key: 'u', ctrlKey: true },
            { key: 'p', ctrlKey: true },
            { key: 'r', ctrlKey: true },
            { key: 'a', ctrlKey: true },
            { key: 'n', ctrlKey: true },
            { key: 't', ctrlKey: true },
            { key: 's', ctrlKey: true },
            { key: 'o', ctrlKey: true },
            { key: 'j', ctrlKey: true },
      ];

      forbiddenKeys.forEach(forbiddenKey => {
            if (
                  e.key === forbiddenKey.key &&
                  (forbiddenKey.ctrlKey === undefined || e.ctrlKey === forbiddenKey.ctrlKey) &&
                  (forbiddenKey.shiftKey === undefined || e.shiftKey === forbiddenKey.shiftKey)
            ) {
                  e.preventDefault();
                  return false; // Stop event propagation
            }
      });
};

// Fetch data from Python's eel function and display results
async function getData() {
      eel.sendData()(function (response) {

            try {
                  response[1].forEach((item, index) => {
                        console.log(item)
                        document.getElementById('all-link').insertAdjacentHTML('beforeend', `<td>${index + 1} : <a style=" text-decoration:none; color:darkblue;" target="_blank" href="${item}">${item} </a>   </td>`)
                  });
                  response[2].forEach((item, index) => {
                        console.log(item)
                        document.getElementById('first-link').insertAdjacentHTML('beforeend', `<td> ${index + 1} : <a style=" text-decoration:none; color:darkblue;" target="_blank" href="${item}">${item} </a>`)
                  });
                  response[3].forEach((item, index) => {
                        console.log(item)
                        document.getElementById('second-link').insertAdjacentHTML('beforeend', `<td> ${index + 1} : <a style=" text-decoration:none; color:darkblue;" target="_blank" href="${item}">${item} </a>`)
                  });
                  document.getElementById('all').style.display = 'block'
                  document.getElementById('first').style.display = 'block'
                  document.getElementById('second').style.display = 'block'
                  document.getElementById('result').innerText = 'Result'
                  // document.getElementById('result').style.backgroundColor = 'cyan'
            }
            catch (err) {
                  console.log(err)
            }

      })
}

// Trigger search and disable button during the process
async function search() {
      var pdf_name = document.getElementById("pdf-name").value
      var location = document.getElementById("location").value
      const submitButton = document.getElementById('btn');
      if (submitButton) {
            submitButton.disabled = true;
      }
      document.getElementById('log').style.display = 'block'
      document.getElementById('result').innerText = ''
      state = 1
      eel.scrape(pdf_name, location)(callBack);
}
// Update status log
function update_status(status) {
      console.log(status);
      document.getElementById('log-list').insertAdjacentHTML('beforeend', `>>> ${status} <br>`);
}

// Callback for handling scrape response
function callBack(response) {
      state = 0
      const submitButton = document.getElementById('btn');
      if (submitButton) {
            submitButton.disabled = false;
      }

      const resultElement = document.getElementById('result');
      const logElement = document.getElementById('log');

      if (response[0] === 2) {
            window.location.href = 'main.html';
      }
      else if (response[0] == 0) {
            resultElement.innerText = response[1];
            resultElement.style.backgroundColor = 'red';
            document.getElementById('log-list').insertAdjacentHTML('beforeend', ``)
            document.getElementById('log').style.display = 'none'
            // document.getElementById('result').innerText = 'Path does not exist! make sure folder that you choose exist or path is Right'
      }
      else {
            resultElement.innerText = response[1];
            resultElement.style.backgroundColor = 'red';
            document.getElementById('log-list').insertAdjacentHTML('beforeend', ``)
            document.getElementById('log').style.display = 'none'
      }
}

window.addEventListener('beforeunload', function (e) {
      if (state == 1) {
            e.preventDefault();
      }
});