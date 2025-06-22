import { createI18n } from 'vue-i18n'
import en from './en.json'
import ru from './ru.json'
import uz from './uz.json'

const savedLang = localStorage.getItem('lang') || 'uz'

const i18n = createI18n({
  legacy: false,
  locale: savedLang,
  fallbackLocale: 'en',
  messages: {
    en,
    ru,
    uz
  }
})

export default i18n
