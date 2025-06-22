const Logo = () => {
  return (
    <div className="w-full max-w-[220px] text-center text-xs font-medium">
      <div className="border border-white/20 rounded-xl p-3 hover:shadow-md transition duration-200">
        <div className="flex flex-col items-center">
          <svg
            className="w-10 h-10 mb-1"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g id="SVGRepo_bgCarrier" strokeWidth="0"></g>
            <g
              id="SVGRepo_tracerCarrier"
              strokeLinecap="round"
              strokeLinejoin="round"
            ></g>
            <g id="SVGRepo_iconCarrier">
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M2 6C2 2.68629 4.68629 0 8 0C11.3137 0 14 2.68629 14 6V16H12L10 14L8 16L6 14L4 16H2V6ZM7 6C7 6.55228 6.55228 7 6 7C5.44772 7 5 6.55228 5 6C5 5.44772 5.44772 5 6 5C6.55228 5 7 5.44772 7 6ZM10 7C10.5523 7 11 6.55228 11 6C11 5.44772 10.5523 5 10 5C9.44772 5 9 5.44772 9 6C9 6.55228 9.44772 7 10 7Z"
                fill="white"
              />
            </g>
          </svg>
          <p className="break-words whitespace-normal leading-tight px-1">
            Análisis Numérico UTN FRSF
          </p>
        </div>
      </div>
    </div>
  );
};

export default Logo;
