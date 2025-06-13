export const validCrewMembers = [
  { name: "Astar", role: "crew" },
  { name: "Nova", role: "crew" },
  { name: "Vega", role: "engineer" },
  { name: "Lyra", role: "crew" },
  { name: "Nebula", role: "crew" },
  { name: "Orion", role: "crew" },
  { name: "Zephyr", role: "pilot" },
  { name: "Cosmos", role: "scientist" },
  { name: "Stellar", role: "crew" },
  { name: "Reinhard", role: "commander" },
];

export const findCrewMember = (crewMember: string) => {
  const lowerCrewMember = crewMember.toLowerCase();
  if (lowerCrewMember === "reinhard") return;
  return validCrewMembers.find(
    (member) => member.name.toLowerCase() === lowerCrewMember
  );
};
