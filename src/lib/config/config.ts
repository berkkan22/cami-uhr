
export const config = {
  header: true,
  headerNames: true,
  dateOneLiner: true,
  camiName: 'DITIB Lüneburg Merkez',
  prayerJson: '/time_data.json',
  dateJson: '/date_data.json',
  quotes: true,
  ditib: true,
  showSabahNamazi: true,
  showAnnouncements: true,
  changeIslamicDayOnMidnight: true,

  camiNameIdentifier: 'lueneburg-merkez-mosque',
  apiUrl: import.meta.env.VITE_API_URL,
  wsUrl: import.meta.env.VITE_WS_URL,
}