"use client";

import { signOut, useSession } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { LogOut, User } from "lucide-react";

export function Navbar() {
  const { data: session } = useSession();

  return (
    <div className="flex h-16 items-center justify-between border-b bg-card px-6">
      <div>
        <h2 className="text-lg font-semibold">
          Bem-vindo, {session?.user?.name || "Usuário"}
        </h2>
        <p className="text-sm text-muted-foreground">{session?.user?.email}</p>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
            <User className="h-4 w-4 text-primary" />
          </div>
          <div className="text-sm">
            <p className="font-medium">{session?.user?.name}</p>
            <p className="text-xs text-muted-foreground capitalize">
              {session?.user?.role?.toLowerCase()}
            </p>
          </div>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={() => signOut({ callbackUrl: "/login" })}
        >
          <LogOut className="h-4 w-4 mr-2" />
          Sair
        </Button>
      </div>
    </div>
  );
}
