import { Injectable } from '@nestjs/common';
import { PrismaClient} from '@prisma/client';

@Injectable()
export class CountriesService {
    private prisma = new PrismaClient();

    async getAllCountries() {
        try {
            return await this.prisma.countries.findMany(); // Adjusted to 'countries'
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async getCountryById(id: string) {
        try {
            return await this.prisma.countries.findUnique({ // Adjusted to 'countries'
                where: { id }
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async createCountry(countryData: any) {
        try {
            return await this.prisma.countries.create({
                data: countryData
            });
        } catch (error) {
            console.error("Error creating country:", error);
            throw error;
        }
    }
    

    async updateCountry(id: string, countryData: any) {
        try {
            return await this.prisma.countries.update({ // Adjusted to 'countries'
                where: { id },
                data: countryData
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }

    async deleteCountry(id: string) {
        try {
            return await this.prisma.countries.delete({ // Adjusted to 'countries'
                where: { id }
            });
        } catch (error) {
            // handle or log the error
            throw error;
        }
    }
}
