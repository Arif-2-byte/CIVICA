export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 flex flex-col items-center justify-center px-6">
      <h1 className="text-6xl font-bold text-blue-900">
        CIVICA
      </h1>

      <p className="mt-6 text-2xl text-gray-700 text-center">
        Your AI-Powered UPSC Current Affairs Companion
      </p>

      <button className="mt-10 rounded-lg bg-blue-900 px-8 py-4 text-white text-lg hover:bg-blue-800 transition">
        Get Started
      </button>
    </main>
  );
}