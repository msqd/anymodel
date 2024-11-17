import { createRootRoute, Link, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtoolsPanel } from "@tanstack/router-devtools";
import { useState } from "react";
import { ReactQueryDevtoolsPanel } from "@tanstack/react-query-devtools";

export const Route = createRootRoute({
  component: () => {
    const [devtool, setDevtool] = useState<null | "router" | "query">(null);
    return (
      <>
        <div className="p-2 flex gap-2">
          <Link to="/" activeProps={{ className: "font-bold" }}>
            Home
          </Link>{" "}
          <Link to="/contacts" activeProps={{ className: "font-bold" }}>
            Contacts
          </Link>
        </div>
        <hr />
        <Outlet />
        <div
          style={{
            position: "fixed",
            bottom: 0,
            right: 0,
            width: devtool !== null ? "100vw" : "auto",
          }}
        >
          <div style={{ textAlign: "right" }}>
            <button
              onClick={() => setDevtool(devtool === "router" ? null : "router")}
              style={{ fontWeight: devtool === "router" ? "bold" : "normal" }}
            >
              router
            </button>
            <button
              onClick={() => setDevtool(devtool === "query" ? null : "query")}
              style={{ fontWeight: devtool === "query" ? "bold" : "normal" }}
            >
              query
            </button>
          </div>
          {devtool === "router" ? (
            <TanStackRouterDevtoolsPanel
              setIsOpen={(value) =>
                value ? setDevtool("router") : setDevtool(null)
              }
              isOpen={devtool === "router"}
            />
          ) : null}
          {devtool === "query" ? <ReactQueryDevtoolsPanel /> : null}
          <div style={{ maxHeight: "40vh" }}></div>
        </div>
      </>
    );
  },
});
