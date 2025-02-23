"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Dumbbell, Users, CreditCard, BarChart3, Calendar, Smartphone, Shield, Clock, Check } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"
import { LanguageToggle } from "@/components/language-toggle"
import { useLanguage } from "@/lib/hooks/use-language"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { useEffect } from "react"

export default function LandingPage() {
  const { t } = useLanguage()

  useEffect(() => {
    const handleNavClick = (e: MouseEvent) => {
      const target = e.target as HTMLAnchorElement
      if (target.hash) {
        e.preventDefault()
        const element = document.querySelector(target.hash)
        if (element) {
          element.scrollIntoView({ behavior: "smooth" })
        }
      }
    }

    document.querySelectorAll('nav a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", handleNavClick)
    })

    return () => {
      document.querySelectorAll('nav a[href^="#"]').forEach((anchor) => {
        anchor.removeEventListener("click", handleNavClick)
      })
    }
  }, [])

  const plans = [
    {
      name: t("pricing.basic.name"),
      price: t("pricing.basic.price"),
      description: t("pricing.basic.description"),
      features: [t("pricing.basic.feature1"), t("pricing.basic.feature2"), t("pricing.basic.feature3")],
    },
    {
      name: t("pricing.pro.name"),
      price: t("pricing.pro.price"),
      description: t("pricing.pro.description"),
      features: [
        t("pricing.pro.feature1"),
        t("pricing.pro.feature2"),
        t("pricing.pro.feature3"),
        t("pricing.pro.feature4"),
      ],
    },
    {
      name: t("pricing.enterprise.name"),
      price: t("pricing.enterprise.price"),
      description: t("pricing.enterprise.description"),
      features: [
        t("pricing.enterprise.feature1"),
        t("pricing.enterprise.feature2"),
        t("pricing.enterprise.feature3"),
        t("pricing.enterprise.feature4"),
        t("pricing.enterprise.feature5"),
      ],
    },
  ]

  const testimonials = [
    {
      name: t("testimonials.person1.name"),
      role: t("testimonials.person1.role"),
      content: t("testimonials.person1.content"),
      avatar: "/avatars/avatar1.jpg",
    },
    {
      name: t("testimonials.person2.name"),
      role: t("testimonials.person2.role"),
      content: t("testimonials.person2.content"),
      avatar: "/avatars/avatar2.jpg",
    },
    {
      name: t("testimonials.person3.name"),
      role: t("testimonials.person3.role"),
      content: t("testimonials.person3.content"),
      avatar: "/avatars/avatar3.jpg",
    },
    {
      name: t("testimonials.person4.name"),
      role: t("testimonials.person4.role"),
      content: t("testimonials.person4.content"),
      avatar: "/avatars/avatar4.jpg",
    },
  ]

  const blogPosts = [
    {
      title: t("blog.post1.title"),
      excerpt: t("blog.post1.excerpt"),
      date: t("blog.post1.date"),
      slug: "post-1",
    },
    {
      title: t("blog.post2.title"),
      excerpt: t("blog.post2.excerpt"),
      date: t("blog.post2.date"),
      slug: "post-2",
    },
    {
      title: t("blog.post3.title"),
      excerpt: t("blog.post3.excerpt"),
      date: t("blog.post3.date"),
      slug: "post-3",
    },
  ]

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Dumbbell className="h-6 w-6 text-orange-500" />
            <span className="text-xl font-bold">EzTo</span>
          </div>
          <nav className="hidden md:flex gap-6">
            <a href="#features" className="text-sm font-medium hover:text-orange-500">
              {t("nav.features")}
            </a>
            <a href="#pricing" className="text-sm font-medium hover:text-orange-500">
              {t("nav.pricing")}
            </a>
            <a href="#testimonials" className="text-sm font-medium hover:text-orange-500">
              {t("nav.testimonials")}
            </a>
            <a href="#blog" className="text-sm font-medium hover:text-orange-500">
              {t("nav.blog")}
            </a>
          </nav>
          <div className="flex items-center gap-2">
            <LanguageToggle />
            <ThemeToggle />
            <Link href="/login">
              <Button variant="ghost">{t("common.signIn")}</Button>
            </Link>
            <Link href="/register">
              <Button className="bg-orange-500 text-white hover:bg-orange-600">{t("common.signUp")}</Button>
            </Link>
          </div>
        </div>
      </header>
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gray-900 dark:bg-gray-950">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center gap-4 text-center">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none text-white">
                {t("landing.hero.title")}
              </h1>
              <p className="mx-auto max-w-[700px] text-gray-400 md:text-xl">{t("landing.hero.subtitle")}</p>
              <div className="flex flex-col gap-2 min-[400px]:flex-row">
                <Button className="bg-orange-500 text-white hover:bg-orange-600">{t("landing.hero.demo")}</Button>
                <Button
                  variant="outline"
                  className="bg-transparent text-white border-white hover:bg-white hover:text-gray-900 dark:text-gray-200 dark:border-gray-200 dark:hover:bg-gray-200 dark:hover:text-gray-900"
                >
                  {t("landing.hero.plans")}
                </Button>
              </div>
            </div>
          </div>
        </section>
        {/* Features Section */}
        <section id="features" className="w-full py-12 md:py-24 lg:py-32 bg-white dark:bg-gray-900">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter text-center mb-12">{t("landing.features.title")}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Feature Cards */}
              <Card className="bg-white dark:bg-gray-800">
                <CardContent className="p-6">
                  <Users className="h-12 w-12 text-orange-500 mb-4" />
                  <h3 className="text-xl font-bold mb-2">{t("landing.features.users.title")}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{t("landing.features.users.description")}</p>
                  <ul className="mt-4 space-y-2">
                    <li className="flex items-center">
                      <Shield className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.users.point1")}</span>
                    </li>
                    <li className="flex items-center">
                      <Clock className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.users.point2")}</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
              <Card className="bg-white dark:bg-gray-800">
                <CardContent className="p-6">
                  <CreditCard className="h-12 w-12 text-orange-500 mb-4" />
                  <h3 className="text-xl font-bold mb-2">{t("landing.features.payments.title")}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{t("landing.features.payments.description")}</p>
                  <ul className="mt-4 space-y-2">
                    <li className="flex items-center">
                      <Shield className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.payments.point1")}</span>
                    </li>
                    <li className="flex items-center">
                      <Clock className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.payments.point2")}</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
              <Card className="bg-white dark:bg-gray-800">
                <CardContent className="p-6">
                  <BarChart3 className="h-12 w-12 text-orange-500 mb-4" />
                  <h3 className="text-xl font-bold mb-2">{t("landing.features.stats.title")}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{t("landing.features.stats.description")}</p>
                  <ul className="mt-4 space-y-2">
                    <li className="flex items-center">
                      <Shield className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.stats.point1")}</span>
                    </li>
                    <li className="flex items-center">
                      <Clock className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.stats.point2")}</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
              <Card className="bg-white dark:bg-gray-800">
                <CardContent className="p-6">
                  <Calendar className="h-12 w-12 text-orange-500 mb-4" />
                  <h3 className="text-xl font-bold mb-2">{t("landing.features.bookings.title")}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{t("landing.features.bookings.description")}</p>
                  <ul className="mt-4 space-y-2">
                    <li className="flex items-center">
                      <Shield className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.bookings.point1")}</span>
                    </li>
                    <li className="flex items-center">
                      <Clock className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.bookings.point2")}</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
              <Card className="bg-white dark:bg-gray-800">
                <CardContent className="p-6">
                  <Smartphone className="h-12 w-12 text-orange-500 mb-4" />
                  <h3 className="text-xl font-bold mb-2">{t("landing.features.mobile.title")}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{t("landing.features.mobile.description")}</p>
                  <ul className="mt-4 space-y-2">
                    <li className="flex items-center">
                      <Shield className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.mobile.point1")}</span>
                    </li>
                    <li className="flex items-center">
                      <Clock className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.mobile.point2")}</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
              <Card className="bg-white dark:bg-gray-800">
                <CardContent className="p-6">
                  <Shield className="h-12 w-12 text-orange-500 mb-4" />
                  <h3 className="text-xl font-bold mb-2">{t("landing.features.security.title")}</h3>
                  <p className="text-gray-600 dark:text-gray-300">{t("landing.features.security.description")}</p>
                  <ul className="mt-4 space-y-2">
                    <li className="flex items-center">
                      <Shield className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.security.point1")}</span>
                    </li>
                    <li className="flex items-center">
                      <Clock className="h-5 w-5 text-green-500 mr-2" />
                      <span>{t("landing.features.security.point2")}</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
        {/* Pricing Section */}
        <section id="pricing" className="w-full py-12 md:py-24 lg:py-32 bg-gray-100 dark:bg-gray-800">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter text-center mb-12">{t("pricing.title")}</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {plans.map((plan) => (
                <Card key={plan.name} className="flex flex-col">
                  <CardHeader>
                    <CardTitle>{plan.name}</CardTitle>
                    <CardDescription>{plan.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="flex-grow">
                    <p className="text-3xl font-bold mb-4">{plan.price}</p>
                    <ul className="space-y-2">
                      {plan.features.map((feature, index) => (
                        <li key={index} className="flex items-center">
                          <Check className="mr-2 h-4 w-4 text-green-500" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                  <CardFooter>
                    <Button className="w-full">{t("pricing.selectPlan")}</Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
            <div className="text-center mt-12">
              <p className="mb-4">{t("pricing.customPlan")}</p>
              <Link href="/contact">
                <Button variant="outline">{t("pricing.contactUs")}</Button>
              </Link>
            </div>
          </div>
        </section>
        {/* Testimonials Section */}
        <section id="testimonials" className="w-full py-12 md:py-24 lg:py-32 bg-white dark:bg-gray-900">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter text-center mb-12">{t("testimonials.title")}</h2>
            <div className="grid md:grid-cols-2 gap-8">
              {testimonials.map((testimonial, index) => (
                <Card key={index} className="flex flex-col">
                  <CardContent className="pt-6">
                    <div className="flex items-center mb-4">
                      <Avatar className="h-12 w-12 mr-4">
                        <AvatarImage src={testimonial.avatar} alt={testimonial.name} />
                        <AvatarFallback>
                          {testimonial.name
                            .split(" ")
                            .map((n) => n[0])
                            .join("")}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <h3 className="font-semibold">{testimonial.name}</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">{testimonial.role}</p>
                      </div>
                    </div>
                    <p className="text-gray-700 dark:text-gray-300">{testimonial.content}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
        {/* Blog Section */}
        <section id="blog" className="w-full py-12 md:py-24 lg:py-32 bg-gray-100 dark:bg-gray-800">
          <div className="container px-4 md:px-6">
            <h2 className="text-3xl font-bold tracking-tighter text-center mb-12">{t("blog.title")}</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {blogPosts.map((post, index) => (
                <Card key={index} className="flex flex-col">
                  <CardHeader>
                    <CardTitle>{post.title}</CardTitle>
                  </CardHeader>
                  <CardContent className="flex-grow">
                    <p className="text-gray-500 dark:text-gray-400 mb-2">{post.date}</p>
                    <p className="text-gray-700 dark:text-gray-300 mb-4">{post.excerpt}</p>
                    <Link href={`/blog/${post.slug}`} className="text-orange-500 hover:underline">
                      {t("blog.readMore")}
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
      </main>
      <footer className="w-full border-t bg-gray-900 py-6">
        <div className="container flex flex-col md:flex-row justify-between items-center gap-4 px-4 md:px-6">
          <div className="flex items-center gap-2">
            <Dumbbell className="h-6 w-6 text-orange-500" />
            <span className="text-xl font-bold text-white">GymFlow</span>
          </div>
          <p className="text-sm text-gray-400">{t("footer.copyright")}</p>
        </div>
      </footer>
    </div>
  )
}

