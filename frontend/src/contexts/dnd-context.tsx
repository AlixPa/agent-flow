import React, { createContext, useContext, useState } from 'react';

type DnDContextValues = [string | null, React.Dispatch<React.SetStateAction<string | null>> ]

const DnDContext = createContext<DnDContextValues>([null, () => {}]);

export const DnDProvider = ({ children }: {children: React.ReactNode}) => {
  const [type, setType] = useState<string | null>(null);

  return (
    <DnDContext.Provider value={[type, setType]}>
      {children}
    </DnDContext.Provider>
  );
}

export default DnDContext;

export const useDnD = () => {
  return useContext(DnDContext);
}