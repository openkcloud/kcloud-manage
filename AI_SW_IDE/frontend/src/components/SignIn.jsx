import { useState } from "react";
import { Typography, Input, Button, Card } from "@material-tailwind/react";
import { EyeSlashIcon, EyeIcon } from "@heroicons/react/24/solid";

export function SignInPage() {
  const [passwordShown, setPasswordShown] = useState(false);
  const togglePasswordVisiblity = () => setPasswordShown((cur) => !cur);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 h-screen">
      {/* Left: Sign In Form */}
      <div className="flex flex-col justify-center items-center p-8">
        <div className="w-full max-w-md">
          <Typography variant="h3" color="blue-gray" className="mb-2 text-2xl font-medium">
            Sign In
          </Typography>
          <Typography className="mb-16 text-gray-600 font-normal text-[18px]">
            Enter your email and password to sign in
          </Typography>
          <form action="#" className="text-left">
            <div className="mb-6">
              <label htmlFor="email">
                <Typography variant="small" className="mb-2 block font-medium text-gray-900">
                  Email
                </Typography>
              </label>
              <Input
                id="email"
                color="gray"
                type="email"
                name="email"
                placeholder="name@mail.com"
                className="w-full placeholder:opacity-100 focus:border-t-primary border-t-blue-gray-200 rounded-lg pl-4"
                labelProps={{ className: "hidden" }}
              />
            </div>
            <div className="mb-6">
              <label htmlFor="password">
                <Typography variant="small" className="mb-2 block font-medium text-gray-900">
                  Password
                </Typography>
              </label>
              <div className="relative">
                <Input
                  placeholder="********"
                  labelProps={{ className: "hidden" }}
                  className="w-full placeholder:opacity-100 focus:border-t-primary border-t-blue-gray-200 rounded-lg pr-10 pl-4"
                  type={passwordShown ? "text" : "password"}
                />
                <div
                  className="absolute inset-y-0 right-0 flex items-center pr-3 cursor-pointer"
                  onClick={togglePasswordVisiblity}
                >
                  {passwordShown ? (
                    <EyeIcon className="h-5 w-5 text-gray-600" />
                  ) : (
                    <EyeSlashIcon className="h-5 w-5 text-gray-600" />
                  )}
                </div>
              </div>
            </div>
            <div className="flex justify-between items-center mb-6">
              <label className="flex items-center">
                <input type="checkbox" className="mr-2" />
                Remember Me
              </label>
              <Typography as="a" href="#" color="blue-gray" variant="small" className="font-medium">
                Forgot password
              </Typography>
            </div>
            <div>
              <Button 
                // color="blue" 
                size="lg" 
                fullWidth 
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              >
                SIGN IN
              </Button>
            </div>
          </form>
        </div>
      </div>

      {/* Right: Information Section */}
      <div className="hidden md:flex flex-col justify-center p-12 bg-black bg-[url('https://www.material-tailwind.com/image/dark-image.png')] bg-cover bg-center rounded-tl-3xl rounded-bl-3xl">
        <Typography variant="h3" className="mb-2 text-4xl font-bold text-white">
          Welcome to
        </Typography>
        <Typography variant="h3" className="mb-2 text-4xl font-bold text-blue-700">
          AI SOFTWARE IDE
        </Typography>
        <Typography variant="h3" className="mb-6 text-4xl font-bold text-blue-700">
          GPU Dashboard!
        </Typography>
        <Typography className="mb-20 text-white leading-loose">
          AI_SW_IDE는 사용 중인 GPU 자원을 실시간으로 모니터링하고, 사용 가능한 GPU 서버를 직접 배포하실 수 있는 웹 페이지입니다. 
          GPU의 사용량, 메모리 상태 등을 한눈에 확인하실 수 있으며, 원하는 설정에 맞춰 새로운 GPU 서버를 손쉽게 생성할 수 있어 연구나 개발 환경에서 자원을 보다 효율적으로 관리하고 활용하실 수 있습니다.
        </Typography>
        <Typography className="mb-10 text-white">
          <strong className="underline">만든이 및 관리</strong>
          <br />오케스트로 &gt; 인공지능연구소 &gt; AI응용팀 &gt; AI응용파트 &gt; <strong className="text-blue-300">yb.jo</strong>
        </Typography>

        <div className="flex items-center gap-2 text-white">
          <span className="text-yellow-400 text-xl">★★★★★★★★</span>
          <Typography>OpenKcloud</Typography>
        </div>
      </div>
    </div>
  );
}

export default SignInPage;