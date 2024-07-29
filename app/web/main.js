function getData() {
      eel.sendData()(function (response) {

            try {
                  console.log(response)


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

            }
            catch (err) {
                  console.log(err)
            }

      })

}


async function search() {
      var pdf_name = document.getElementById("pdf-name").value;
      var location = document.getElementById("location").value;
      const submitButton = document.getElementById('btn');
      if (submitButton) {
            submitButton.disabled = true;
            console.log('licked')
      }
      document.getElementById('log').style.display = 'block'
      document.getElementById('result').innerText = ''



      eel.scrape(pdf_name, location)(call_Back);
}

function update_status(status) {
      console.log(status)

      document.getElementById('log-list').insertAdjacentHTML('beforeend', `:: ${status} <br>`)


}



function call_Back(response) {
      // document.getElementById('log').style.display = 'none'

      console.log(response)
      const submitButton = document.getElementById('btn');
      if (submitButton) {
            submitButton.disabled = false;
            console.log('licked')

      }
      if (response[0] == 2) {
            window.location.href = 'main.html'
      }
      else if (response[0] == 0) {
            console.log('its zero')
            document.getElementById('log').style.display = 'none'
            document.getElementById('result').style.backgroundColor = 'red'
            document.getElementById('result').innerText = 'Path does not exist! make sure folder that you choose exist or path is Right'

      }
      else {

            console.log('its one')
            document.getElementById('result').innerText = 'something went wrong'
            document.getElementById('result').style.backgroundColor = 'red'
            document.getElementById('log').style.display = 'none'




      }



}




