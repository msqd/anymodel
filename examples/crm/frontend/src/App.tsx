import './App.css'
import {useQuery} from "react-query";

function useContacts() {
    return useQuery('contacts', async () => {
        const response = await fetch('http://localhost:3001/')
        if (!response.ok) {
            throw new Error('Network response was not ok')
        }
        return response.json()
    })

}

function App() {
    const contactsQuery = useContacts()

    if (contactsQuery.isLoading) {
        return 'Loading...'
    }
    if (contactsQuery.isError) {
        return `An error has occurred.`
    }

    return (
        <>
            {contactsQuery.data.map((contact: any) => (
                <div key={contact.id}>
                    {contact.first_name} {contact.last_name} &lt;{contact.email}&gt;
                </div>
            ))}
        </>
    )
}

export default App
