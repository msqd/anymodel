import { createLazyFileRoute, Link, Outlet } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/contacts")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <>
      <div className="p-2 flex gap-2">
        <Link
          to="/contacts"
          activeProps={{ className: "font-bold" }}
          activeOptions={{ exact: true }}
        >
          List
        </Link>{" "}
        <Link to="/contacts/create" activeProps={{ className: "font-bold" }}>
          Create
        </Link>
      </div>
      <hr />
      <Outlet />
    </>
  );
}
