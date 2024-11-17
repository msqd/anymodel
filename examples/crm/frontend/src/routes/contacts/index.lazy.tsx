import { createLazyFileRoute, Link } from "@tanstack/react-router";
import { useContactListQuery } from "src/queries/contacts";

export const Route = createLazyFileRoute("/contacts/")({
  component: () => {
    const contactsQuery = useContactListQuery();

    if (contactsQuery.isLoading) {
      return "Loading...";
    }
    if (contactsQuery.isError) {
      return `An error has occurred.`;
    }

    return (
      <main>
        <h1>Contacts</h1>
        {contactsQuery.data.map((contact: any) => (
          <div key={contact.id}>
            #{contact.id}{" "}
            <Link to={`/contacts/${contact.id}`}>
              {contact.first_name} {contact.last_name}
            </Link>{" "}
            &lt;
            {contact.email}&gt;
          </div>
        ))}
      </main>
    );
  },
});
