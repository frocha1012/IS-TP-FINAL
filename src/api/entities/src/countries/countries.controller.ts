import { Controller, Get, Post, Body, Param, Put, Delete } from '@nestjs/common';
import { CountriesService } from './countries.service';

@Controller('countries')
export class CountriesController {
    constructor(private readonly countriesService: CountriesService) {}

    @Get()
    async getAllCountries() {
        return this.countriesService.getAllCountries();
    }

    @Get(':id')
    async getCountryById(@Param('id') id: string) {
        return this.countriesService.getCountryById(id);
    }

    @Post()
    async createCountry(@Body() countryData: { name: string }) {
        return this.countriesService.createCountry(countryData);
    }

    @Put(':id')
    async updateCountry(@Param('id') id: string, @Body() countryData: { name?: string }) {
        return this.countriesService.updateCountry(id, countryData);
    }

    @Delete(':id')
    async deleteCountry(@Param('id') id: string) {
        return this.countriesService.deleteCountry(id);
    }
}
