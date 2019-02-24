const embedElement = document.querySelector('#form')
typeformEmbed.makeWidget(
    embedElement,
    'https://inspiration-hackcu.typeform.com/to/UKTXV4', // NOTE: Replace with your typeform URL
    {
      hideHeaders: true,
      hideFooter: true,
      opacity: 0,
      buttonText: "Find your taste in music!",
      onSubmit: function () {
        console.log('Preferences successfully submitted')
      }
    }
  )