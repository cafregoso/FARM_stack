import React from "react";
import useAuth from "../hooks/useAuth";

const Admin = () => {
  const { auth } = useAuth();

  return (
    <div>
      {auth?.role === "Admin" ? (
        <span className="text-primary text-xl">
          Ok Admin! You are {auth.username} and you seem to be an Admin.
        </span>
      ) : (
        <span>Only admins, sorry</span>
      )}
    </div>
  );
};

export default Admin;
