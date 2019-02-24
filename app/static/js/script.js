const link = document.querySelector('#formLink').innerHTML
const embedElement = document.querySelector('#form')
typeformEmbed.makeWidget(
    embedElement,
    link, // NOTE: Replace with your typeform URL
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