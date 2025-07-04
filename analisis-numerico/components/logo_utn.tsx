const LogoUTN = () => {
  return (
    <div className="w-full max-w-[220px] text-center text-xs font-medium">
      <div className="border border-white/20 rounded-xl p-3 hover:shadow-md transition duration-200">
        <div className="flex flex-col items-center">
          <img src="/logo_utn.svg" alt="Logo UTN" className="w-10 h-10 mb-1" />
          <p className="break-words whitespace-normal leading-tight px-1">
            Facultad Regional Santa Fe
          </p>
        </div>
      </div>
    </div>
  );
};

export default LogoUTN;
